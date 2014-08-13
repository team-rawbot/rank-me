require([
    "jquery",
    "bootstrap",
    "modules/add_result",
    "modules/score_chart"
], function($, Bootstrap, AddResult, ScoreChart) {
    $(function() {
        AddResult.init();
        ScoreChart.drawChart($('#score-chart-container'));
    });
});
