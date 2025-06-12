'use strict';

const fs = require('fs');
const http = require('http');
const vm = require('vm');

/**
 * Fetch http://w00g.kancolle-server.com/gadget_html5/js/kcs_const.js
 *  old: http://203.104.209.7/gadget/js/kcs_const.js
 * Parse and update all `servers.json` files.
 */

// change this if not execute this under `tools` directory
const langFolderRoot = '../data';
const langFolders = [ 'de', 'es', 'fr', 'id', 'it', 'jp', 'kr', 'nl', 'pt', 'ru', 'scn', 'tcn', 'tcn-yue', 'th', 'ua', 'vi' ];
const serverJsonFilename = "servers.json";
const indentChar = '\t';
const bomChar = '\uFEFF';
const kcsConstUrl = "http://w00g.kancolle-server.com/gadget_html5/js/kcs_const.js";

const _eval = (content) => {
	const sandbox = {}, exports = {};
	sandbox.exports = exports;
	sandbox.module = {
		exports: exports,
		filename: module.filename,
		id: module.filename,
		parent: module,
	};
	sandbox.global = sandbox;
	const options = { displayErrors: false };
	const stringScript = String(content).replace(/^\#\!.*/, '');
	const script = new vm.Script(stringScript, options);
	script.runInNewContext(sandbox, options);
	return sandbox.module.exports;
};

const toFormattedJson = (obj, useCrLf = false, addBom = false, ident = indentChar) => {
	const json = JSON.stringify(obj, undefined, ident) + '\n';
	const newlinedJson = useCrLf ? json.replace(/\n/g, '\r\n') : json;
	return addBom ? bomChar + newlinedJson : newlinedJson;
};

const parseWorldServers = (kcsConstJs, lastUpdated) => {
	console.info(`Parsing KCS constants updated on ${lastUpdated} ...`);
	const exportsAppend = '\n exports.ConstServerInfo = ConstServerInfo;';
	const kcsContext = _eval(kcsConstJs + exportsAppend);
	const serverInfo = kcsContext.ConstServerInfo;
	//console.info("ConstServerInfo:", serverInfo);
	const servers = {};
	for (const key of Object.keys(serverInfo)) {
		const world = key.match(/^World_(\d+)$/);
		if (world && world[1]) {
			const num = Number(world[1]);
			const host = serverInfo[key].match(/^https?:\/\/(.+)\/$/)[1];
			const isDomain = !!host.match(/^w\d+\w+\.kancolle-server\.com/);
			const isHttps = !!serverInfo[key].match(/^https:/);
			servers[num] = {
				"num": num,
				"host": host,
				"domain": isDomain,
				"https": isHttps
			};
		}
	}
	console.info("Parsed servers:\n", servers);
	return servers;
};

const updateServersJson = (servers) => {
	console.info(`Updating '${serverJsonFilename}' for 'en' ...`);
	const enFilename = `${langFolderRoot}/en/${serverJsonFilename}`;
	const oldEnServers = JSON.parse(fs.readFileSync(enFilename, 'utf8'));
	const newEnServers = {};
	for (const num of Object.keys(servers)) {
		for (const server of Object.keys(oldEnServers)) {
			const newServer = servers[num];
			const oldServer = oldEnServers[server];
			const hostname = newServer.host;
			if (num == oldServer.num) {
				newEnServers[hostname] = oldServer;
				newEnServers[hostname].num = newServer.num;
				if (newServer.domain) {
					newEnServers[hostname].domain = newServer.host;
					newEnServers[hostname].https = newServer.https;
				} else {
					newEnServers[hostname].ip = newServer.host;
				}
			}
		}
	}
	//console.info(oldEnServers)
	fs.writeFileSync(enFilename, toFormattedJson(newEnServers, true), 'utf8');
	console.info(`'en/${serverJsonFilename}' file updated`);

	for (const lang of langFolders) {
		console.info(`Updating '${serverJsonFilename}' for '${lang}' ...`);
		const filename = `${langFolderRoot}/${lang}/${serverJsonFilename}`;
		let json = fs.readFileSync(filename, 'utf8');
		const bomRegex = new RegExp('^' + bomChar);
		// force all UTF-8 files without BOM
		const isBom = false;
		//const isBom = bomRegex.test(json);
		// remove BOM to parse JSON avoiding error
		json = json.replace(bomRegex, '');
		// use CRLF newline if file is, otherwise use LF only
		const isCrLf = /\r\n/.test(json);
		const oldServers = JSON.parse(json);
		const newServers = {};
		for (const enKey of Object.keys(newEnServers)) {
			const enOldIp = newEnServers[enKey].ip;
			for (const oldKey of Object.keys(oldServers)) {
				if (enKey == oldKey || enOldIp == oldKey) {
					newServers[enKey] = oldServers[oldKey];
				}
			}
		}
		//console.info(newServers)
		fs.writeFileSync(filename, toFormattedJson(newServers, isCrLf, isBom), 'utf8');
		console.info(`'${lang}/${serverJsonFilename}' file updated`);
	}
};

console.info(`Fetching KCS constants from '${kcsConstUrl}' ...`);
http.get(kcsConstUrl, (res) => {
	const { statusCode } = res;
	//const contentType = res.headers['content-type'];
	const lastUpdated = res.headers.date;
	if (statusCode !== 200) {
		console.error(new Error(`Unexpected response status: ${statusCode}`));
		res.resume();
		return;
	}
	//res.setEncoding('utf8');
	let rawData = '';
	res.on('data', (chunk) => { rawData += String(chunk); });
	res.on('end', () => { updateServersJson(parseWorldServers(rawData, lastUpdated)); });
}).on('error', (e) => {
	console.error(e);
});
