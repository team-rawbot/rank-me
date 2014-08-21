define(["jquery", "underscore", "highcharts"], function($, _, HighCharts) {
    var ScoreChart = function ($) {
        var drawChart,
            mapToPosition,
            positionSeries,
            getNbGames,
            getSeries,
            yAxis,
            mode;

        mode = 'position';

        mapToPosition = function(element, index) {
            return {
                'x': index,
                'y': element[mode],
                'skill': Math.round(element['skill'] * 100) / 100,
                'position': element['position'],
                'marker': {
                    'radius': element['played']? 5:0,
                    'fillColor': element['win']? null:'#fff'
                }
            };
        };

        drawChart = function($target) {
            if(window.location.hash === '#skill') {
                mode = 'skill';
            }

            var scoresByTeam = $target.data('scores');

            var positionSeries = getSeries(scoresByTeam);
            var nbGames = getNbGames(scoresByTeam);

            // sort series by team name
            positionSeries = _.sortBy(positionSeries, 'name');

            yAxis = {
                'skill': {
                    title: {
                        text: 'Skill'
                    },
                    gridLineWidth: 0,
                    tickPixelInterval: 1,
                    startOnTick: true,
                    endOnTick: true
                },
                'position': {
                    title: {
                        text: 'Position'
                    },
                    reversed: true,
                    gridLineWidth: 0,
                    min: 1,
                    max: positionSeries.length,
                    tickInterval: 1
                }
            };

            $target.highcharts({
                chart: {
                    backgroundColor: 'transparent',
                    zoomType: 'y'
                },
                title: {
                    text: 'Last ' + nbGames + ' games',
                    x: -20 //center
                },
                xAxis: {
                    text: 'Game id',
                    type: 'linear',
                    min: 0,
                    max: nbGames,
                    gridLineColor: '#fff',
                    offset: 30
                },
                yAxis: yAxis[mode],
                tooltip: {
                    valueSuffix: '',
                    crosshairs: true,
                    positioner: function() { return { x: 0, y: 0 }; },
                    useHTML: true,
                    headerFormat: '',
                    pointFormat: '<b>{series.name}</b> : {point.position}, skill : {point.skill}',
                    footerFormat: ''
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

        getNbGames = function(scoresByTeam) {
            for (var team in scoresByTeam) {
                return scoresByTeam[team].length;
            }
        };

        return {
            drawChart: drawChart
        };
    }();

    return ScoreChart;
});
