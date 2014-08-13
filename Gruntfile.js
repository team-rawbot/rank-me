module.exports = function(grunt) {
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-watch");

    grunt.initConfig({
        less: {
            development: {
                options: {
                    paths: ["static/assets/less"],
                    compress : false,
                    yuicompress : false
                },
                files: {
                    "static/main.css": "static/main.less"
                }
            }
        },

        watch: {
            assets: {
                files: "static/**/*.less",
                tasks: ["less"],
                options: {
                    debounceDelay: 250,
                    livereload: true
                }
            }
        },
    });

    // Default task(s).
    grunt.registerTask("default", ["less", "watch"]);
};
