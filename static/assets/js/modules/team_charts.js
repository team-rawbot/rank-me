define(['jquery'], function ($) {
    function init() {
        // HEAD TO HEAD GRAPH
        // ------------------

        // Collect data from the HTML table
        var data = {users: [], wins: [], defeats: []};
        $('#head-2-head-results tbody tr').each(function () {
            data.users.push($(this).find('td:nth-child(1)').text());
            data.wins.push(parseInt($(this).find('td:nth-child(2)').text()));
            data.defeats.push(parseInt($(this).find('td:nth-child(3)').text()));
        });

        // Replace the table by the graph div
        $('#head-2-head-results')
            .after('<div id="head-to-head-charts" />')
            .remove();

        // Init highcharts JS
        $('#head-to-head-charts').highcharts({
            chart: {
                type: 'bar',
                backgroundColor: 'transparent'
            },
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: data.users
            },
            yAxis: {
                min: 0,
                tickInterval: 25,
                title: {
                    text: null
                }
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<b>{point.key}</b><br><br><table>' +
                    '<tr><td><b>Total</b></td><td style="text-align: right"><b>{point.total}</b></td><td>&nbsp;</td></tr>',
                pointFormat: '<tr>' +
                    '<td style="padding: 2px;"><span style="color:{series.color}">{series.name}</span></td>' +
                    '<td style="padding: 2px; text-align: right;"><b>{point.y}</b></td>' +
                    '<td style="padding: 2px; text-align: right;">({point.percentage:.0f}%)</td>' +
                '</tr>',
                footerFormat: '</table>',
                shared: true
            },
            plotOptions: {
                series: {
                    stacking: 'percent'
                }
            },
            series: [
                {
                    name: 'Wins',
                    data: data.wins,
                    color: '#89c571'
                },
                {
                    name: 'Defeats',
                    data: data.defeats,
                    color: '#d76b7a'
                }
            ]
        });

        // GAME PER WEEK GRAPH
        // -------------------

        // Collect data from the HTML table
        var data = {labels: [], games: [], avg: []};
        $('#games-per-week tbody tr').each(function () {
            data.labels.push($(this).find('td:nth-child(1)').text());
            data.games.push(parseInt($(this).find('td:nth-child(2)').text()));
            data.avg.push(parseFloat($(this).find('td:nth-child(4)').text()));
        });

        // Replace the table by the graph div
        $('#games-per-week')
            .after('<div id="games-per-week-charts" />')
            .remove();

        $('#games-per-week-charts').highcharts({
            chart: {
                type: 'column',
                margin: [0, 0, 50, 0],
                backgroundColor: 'transparent',
                height: 170
            },
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: data.labels,
                labels: {
                    enabled: false
                }
            },
            yAxis: {
                maxPadding: 0,
                minPadding: 0
            },
            series: [
                {
                    name: 'Player games',
                    data: data.games,
                    color: '#659dca',
                    pointPadding: 0,
                    groupPadding: 0
                },
                {
                    name: 'Office avg',
                    type: 'spline',
                    data: data.avg,
                    color: '#d76b7a',
                    width: 1
                }
            ]
        });
    }

    return {
        'init': init
    }
});

