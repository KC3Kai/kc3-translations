'use strict';

const fs = require('fs');
const http = require('http');
const vm = require('vm');

/**
 * Fetch http://203.104.209.7/gadget/js/kcs_const.js
 * Parse and update all `servers.json` files.
 */

// change this if not execute this under `tools` directory
const langFolderRoot = '../data';
const langFolders = [ 'de', 'es', 'fr', 'id', 'it', 'jp', 'kr', 'nl', 'pt', 'ru', 'scn', 'tcn', 'tcn-yue', 'th', 'ua', 'vi' ];
const serverJsonFilename = "servers.json";
const indentChar = '\t';
const bomChar = '\uFEFF';
const kcsConstUrl = "http://203.104.209.7/gadget_html5/js/kcs_const.js";

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
	//console.info("ConstServerInfo:", kcsContext.ConstServerInfo)
	const serverInfo = kcsContext.ConstServerInfo;
	const servers = {};
	for (const key of Object.keys(serverInfo)) {
		const world = key.match(/^World_(\d+)$/);
		if (world && world[1]) {
			const num = Number(world[1]);
			const ip = serverInfo[key].match(/^http:\/\/(.+)\/$/)[1];
			servers[num] = ip;
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
			const newIp = servers[num];
			const oldServer = oldEnServers[server];
			if (num == oldServer.num) {
				newEnServers[newIp] = oldServer;
				newEnServers[newIp].ip = newIp;
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
		for (const oldIpKey of Object.keys(oldEnServers)) {
			for (const ip of Object.keys(oldServers)) {
				if (oldIpKey == ip) {
					const newIp = oldEnServers[oldIpKey].ip;
					newServers[newIp] = oldServers[ip];
					if (newServers[newIp].ip) newServers[newIp].ip = newIp;
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
