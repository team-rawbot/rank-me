require([
    "jquery",
    "bootstrap",
    "modules/add_result",
    "modules/team_charts",
    "modules/score_chart"
], function($, Bootstrap, AddResult, TeamChart, ScoreChart) {
    $(function() {
        AddResult.init();
        TeamChart.init();
        ScoreChart.drawChart($('#score-chart-container'));
    });
});
