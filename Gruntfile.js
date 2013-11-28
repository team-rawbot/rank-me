module.exports = function(grunt) {
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-watch");

    grunt.initConfig({
        less: {
            development: {
                options: {
                    paths: ["static/css"],
                    compress : false,
                    yuicompress : false
                },
                files: {
                    "static/main.css": "static/css/*.less"
                }
            }
        },

        watch: {
            assets: {
                files: "static/css/*.less",
                tasks: ["less"],
                options: {
                    debounceDelay: 250,
                }
            }
        },
    });

    // Default task(s).
    grunt.registerTask("default", ["less", "watch"]);
};
