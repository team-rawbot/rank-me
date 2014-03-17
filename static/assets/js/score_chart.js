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
                'radius': element['played']? 5:0,
                'fillColor': element['win']? null:'#fff'
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
            colors: [
                '#1f77b4',
                '#aec7e8',
                '#ff7f0e',
                '#ffbb78',
                '#637939',
                '#8ca252',
                '#b5cf6b',
                '#cedb9c',
                '#8c6d31',
                '#bd9e39',
                '#e7ba52',
                '#e7cb94',
                '#843c39',
                '#ad494a',
                '#d6616b',
                '#e7969c',
                '#7b4173',
                '#a55194',
                '#ce6dbd',
                '#de9ed6'

            ],
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
                    'lineColor': null,
                    'lineWidth': '2px',
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
