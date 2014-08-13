require.config({
    deps: ["init"],
    locale: "en",

    paths: {
        jquery     : "../../vendors/jquery/dist/jquery",
        bootstrap  : "../../vendors/bootstrap/dist/js/bootstrap.min",
        highcharts : "../../vendors/highcharts/highcharts",
        high_exporting: "../../vendors/highcharts/modules/exporting",
        underscore : "../../vendors/underscore/underscore"
    },

    shim: {
        bootstrap: {
            deps: ["jquery"]
        },
        highcharts: {
            deps: ["jquery"]
        },
        high_exporting: {
            deps: ["highcharts"]
        },
        underscore: {
            exports: "_"
        }
    }
});
