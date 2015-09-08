module.exports = function(grunt) {
	
	grunt.initConfig({
		jsonlint: {
			all : {
				options: {},
				src: ['data/**/*.json']
			}
		}
	});
	
	grunt.loadNpmTasks('grunt-jsonlint');
	
};

