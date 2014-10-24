require.config({
    deps: ["init"],
    locale: "en",

    paths: {
        jquery     : "../vendors/jquery/dist/jquery",
        bootstrap  : "../vendors/bootstrap-sass-official/assets/javascripts/bootstrap",
        d3         : "../vendors/d3/d3",
        underscore : "../vendors/underscore/underscore",
        select2    : "../vendors/select2/select2"
    },

    shim: {
        bootstrap: {
            deps: ["jquery", "select2"]
        },
        underscore: {
            exports: "_"
        }
    }
});
