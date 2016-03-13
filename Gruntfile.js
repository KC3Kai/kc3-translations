module.exports = function(grunt) {
	
	grunt.initConfig({
		clean: {
			all: {
				src: [ 'build/**/*' ]
			}
		},
		copy: {
			all : {
				expand: true,
				cwd: 'data/',
				src: '**/*',
				dest: 'build/'
			}
		},
		jsonlint: {
			all : {
				options: {
					format: true
				},
				src: ['build/**/*.json']
			}
		},
		"json-minify": {
			all : {
				files: 'build/**/*.json'
			}
		}
	});
	
	grunt.loadNpmTasks('grunt-jsonlint');
	grunt.loadNpmTasks('grunt-json-minify');
	grunt.loadNpmTasks('grunt-contrib-copy');
	grunt.loadNpmTasks('grunt-contrib-clean');
	
	grunt.registerTask('checks', [
		'clean',
		'copy',
		'jsonlint',
		'json-minify',
		'clean'
	]);
};

