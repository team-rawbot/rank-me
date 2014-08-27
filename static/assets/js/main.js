require.config({
    deps: ["init"],
    locale: "en",

    paths: {
        jquery     : "../../vendors/jquery/dist/jquery",
        bootstrap  : "../../vendors/bootstrap/dist/js/bootstrap.min",
        d3 : "../../vendors/d3/d3",
        underscore : "../../vendors/underscore/underscore"
    },

    shim: {
        bootstrap: {
            deps: ["jquery"]
        },
        underscore: {
            exports: "_"
        }
    }
});
