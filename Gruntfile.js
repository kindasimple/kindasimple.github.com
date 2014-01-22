module.exports = function(grunt) {
	grunt.initConfig({
		shell: {
			bld_dev: {
				command: 'jekyll build'
			},
			srv_dev: {
				command: 'jekyll serve --config _config.yml,_config-dev.yml'
			}
		},	
		watch: {
			files: ['./index.html', '_posts/*', '_drafts/*', '_layouts/*'],
			tasks: ['shell:bld_dev', 'shell:srv_dev'],
			options: {
				interrupt: true,
				atBegin: true,
				livereload: 35729,
				debounceDelay: 1500,
			}	
		}
	});
	grunt.event.on('watch', function(action, filepath, target) {
  		grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
	});
	grunt.loadNpmTasks('grunt-shell');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.registerTask('default', ['shell']);
}
