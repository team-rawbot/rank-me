var ScoreChart = (function ($) {
    var drawChart,
        mapToPosition,
        positionSeries,
        getMinGameId,
        getMaxGameId,
        getSeries;

    mapToPosition = function(element) {
        return {
            'x': element['game'],
            'y': element['position'],
            'marker': {
                'radius': element['played']? 5:0
            }
        };
    };

    drawChart = function($target) {
        var scoresByTeam = $target.data('scores');

        var positionSeries = getSeries(scoresByTeam);
        var minGameId = getMinGameId(scoresByTeam);
        var maxGameId = getMaxGameId(scoresByTeam);

        // sort series by team name
        positionSeries = _.sortBy(positionSeries, 'name');

        $target.highcharts({
            title: {
                text: 'Last ' + (maxGameId - minGameId + 1) + ' games',
                x: -20 //center
            },
            xAxis: {
                text: 'Game id',
                type: 'linear',
                min: minGameId,
                max: maxGameId,
                gridLineColor: '#fff',
                offset: 30
            },
            yAxis: {
                title: {
                    text: 'Position'
                },
                reversed: true,
                gridLineWidth: 0,
                min: 1,
                max: positionSeries.length,
                tickInterval: 1
            },
            tooltip: {
                valueSuffix: ''
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: positionSeries
        });
    };

    getSeries = function(scores_by_team) {
        positionSeries = [];

        for (var team in scores_by_team) {
            var team_scores = scores_by_team[team];
            positionSeries.push({
                'name': team,
                'data': team_scores.map(mapToPosition),
                'marker': {
                    'symbol': 'circle'
                }
            });
        }

        return positionSeries;
    };

    getMinGameId = function(scores_by_team) {
        for (team in scores_by_team) {
            return scores_by_team[team][0]['game'];
        }
    };

    getMaxGameId = function(scores_by_team) {
        for (team in scores_by_team) {
            return scores_by_team[team][scores_by_team[team].length - 1]['game'];
        }
    };

    return {
        drawChart: drawChart
    };
})(jQuery);

$(function() {
    var $target = $('#score-chart-container');
    ScoreChart.drawChart($target);
});
