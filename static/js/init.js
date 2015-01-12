require([
    "jquery",
    "bootstrap",
    "modules/add_result",
    "modules/team_charts",
    "modules/score_chart"
], function($, Bootstrap, AddResult, TeamChart, ScoreChart) {
    $(function() {
        AddResult.init();
        TeamChart.drawChart();
        ScoreChart.drawChart($('#score-chart-container'));

        // togglers
        $('.toggler__handle').on('click', function(e) {
            e.preventDefault();

            $(this).closest(".toggler")
                .find(".toggler__container")
                .toggleClass("visible");

            var text = $(this).text();
            $(this).text($(this).data('toggler'));
            $(this).data('toggler', text);
        })
    });
});
