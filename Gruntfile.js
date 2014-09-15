module.exports = function(grunt) {
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks('grunt-contrib-compass');

    grunt.initConfig({
        compass: {
            dist: {
                options: {
                    sassDir: 'static/sass',
                    cssDir: 'static/css',
                    javascriptsDir: 'static/js',
                    imagesDir: 'static/images',
                }
            }
        },

        watch: {
            sass: {
                files: ['static/sass/*.scss'],
                tasks: ['compass:dist'],
                options: {
                    livereload: true,
                    spawn: false,
                }
            }
        }
    });

    // Default task(s).
    grunt.registerTask("default", ["watch"]);
};
