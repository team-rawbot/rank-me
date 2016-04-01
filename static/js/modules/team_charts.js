import $ from 'jquery';
import d3 from 'd3';

function head2head(container) {
    if(container.length == 0) {
        return;
    }

    var data = [];
    container.find('tbody tr').each(function () {
        var user = $(this).find('td:nth-child(1)').text();
        var wins = parseInt($(this).find('td:nth-child(2)').text());
        var defeats = parseInt($(this).find('td:nth-child(3)').text());
        var fairness = parseFloat($(this).find('td:nth-child(4)').text());
        var total = wins + defeats;

        data.push({
            name: user,
            values: [
                { name: 'wins',     width: 2,  value: wins / total,     tooltip: wins + ' games',    previous: 0 },
                { name: 'defeats',  width: 2,  value: defeats / total,  tooltip: defeats + ' games', previous: wins/total },
                { name: 'total',    width: 6,  value: total,            tooltip: total + ' games',   previous: 0 },
                { name: 'fairness', width: 6,  value: fairness / 100,   tooltip: (Math.round(fairness * 100) / 100) + '%' }
            ]
        });
    });

    var maxTotal = d3.max(data, function(d) { return d.values[2].value; });
    data.map(function(d) {d.values[2].value /= maxTotal; });

    container = container.parent();
    container.empty();

    var margin = {top: 20, right: 20, bottom: 25, left: 130},
        width = container.width() - margin.left - margin.right,
        height = 600;

    var x = d3.scale.linear()
        .rangeRound([0, width]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, height], .3);

    var color = d3.scale.ordinal()
        .range(['#89c571', '#d76b7a', '#659dca', '#e1c170'])
        .domain(['wins', 'defeats', 'total', 'fairness']);

    var svg = d3.select(container[0]).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var names = data.map(function(d) { return d.name; });
    y.domain(names);

    var opponent = svg.selectAll('.opponent')
        .data(data)
        .enter()
        .append('g')
        .attr('class', 'opponent')
        .attr('transform', function (d) {
            return 'translate(0, ' + y(d.name) + ')';
        });

    opponent.selectAll('rect')
        .data(function (d) {
            return d.values;
        })
        .enter()
        .append('rect')
        .attr('height', function(d) { return Math.floor(y.rangeBand() / d.width); })
        .attr('y', function(d) { switch(d.name) {
                case 'total': return Math.floor(y.rangeBand() * (3/4) + 1);
                case 'fairness': return Math.floor(y.rangeBand() / 2 + 3);
                default: return 0;
            }
        })
        .attr('x', function(d) { return x(d.previous ? d.previous : 0); })
        .attr('width', function (d) { return x(d.value); })
        .style('fill', function (d) { return color(d.name); })
        .append('title')
        .text(function (d) { return d.tooltip; });

    var yAxis = d3.svg.axis()
        .scale(y)
        .tickSize(0)
        .tickPadding(5)
        .orient('left');

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .ticks(5)
        .tickFormat(d3.format('.0%'));

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y axis')
        .call(yAxis);

    var legend = svg
        .append('g')
        .attr('class', 'legend')
      .selectAll('rect')
        .data(color.domain())
      .enter()
        .append('g');

    var columns = [0, 80, 185, 265];
    var dotWidth = 15;

    legend.append('circle')
        .attr('cx', function(d, idx) { return columns[idx] })
        .attr('cy', -6)
        .attr('r', 6)
        .style('fill', color);
    legend.append('text')
        .attr('x', function(d, idx) { return columns[idx] + 16 })
        .attr('y', 0)
        .text(function(d) { return d; });
}

function officeAvg(container) {
    if(container.length == 0) {
        return;
    }

    var data = [];
    container.find('tbody tr').each(function () {
        var week = $(this).find('td:nth-child(1)').text();
        var playedGames = parseInt($(this).find('td:nth-child(2)').text());
        var totalGames = parseInt($(this).find('td:nth-child(3)').text());
        var average = parseInt($(this).find('td:nth-child(4)').text());

        data.push({
            week: week,
            playedGames: playedGames,
            totalGames: totalGames,
            average: average
        });
    });

    container = container.parent();
    container.empty();

    var margin = {top: 15, right: 5, bottom: 20, left: 35},
        width = container.width() - margin.left - margin.right,
        height = 200;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], 0.1)
        .domain(data.map(function(d) { return d.week; }));

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.totalGames; })])
        .range([height, 0]);

    var line = d3.svg.line()
        .interpolate('monotone')
        .x(function(d) { return x(d.week) + x.rangeBand() / 2; })
        .y(function(d) { return y(d.totalGames); });

    var lineAvg = d3.svg.line()
        .interpolate('monotone')
        .x(function(d) { return x(d.week) + x.rangeBand() / 2; })
        .y(function(d) { return y(d.average); });

    var svg = d3.select(container[0]).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var yAxis = d3.svg.axis()
        .scale(y)
        .outerTickSize(0)
        .orient('left');

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .tickFormat(function(d) { return 'W ' + d.split('.')[1]; });

    svg.append('g')
        .attr('class', 'y axis')
        .call(yAxis);

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

    var colors = [
        {name: 'player games', color: '#659dca'},
        {name: 'office total', color: '#d76b7a'},
        {name: 'office average', color: '#89c571'}
    ];

    var played = svg.selectAll('.played')
        .data(data)
        .enter()
        .append('g')
        .attr('class', 'played')
        .attr('fill', colors[0].color)
        .attr('transform', function (d) { return 'translate(' + x(d.week) + ', 0)'; });

    played.append('rect')
        .attr('width', x.rangeBand())
        .attr('height', function(d) { return Math.floor(height - y(d.playedGames)); })
        .attr('y', function(d) { return y(d.playedGames); })
        .append('title')
        .text(function (d) { return d.playedGames + ' games'; });

    svg.append('path')
        .datum(data)
        .attr('class', 'line')
        .attr('stroke', colors[1].color)
        .attr('d', line);

    svg.append('path')
        .datum(data)
        .attr('class', 'line')
        .attr('stroke', colors[2].color)
        .attr('d', lineAvg);

    var legend = svg
        .append('g')
        .attr('class', 'legend')
        .selectAll('rect')
        .data(colors)
        .enter()
        .append('g');

    var columns = [0, 150, 280];

    legend.append('circle')
        .attr('cx', function(d, idx) { return columns[idx] })
        .attr('cy', -6)
        .attr('r', 6)
        .style('fill', function(d) { return d.color; });
    legend.append('text')
        .attr('x', function(d, idx) { return columns[idx] + 16 })
        .attr('y', 0)
        .text(function(d) { return d.name; });
}

export function drawChart() {
    head2head($('#head-2-head-results'));
    officeAvg($('#games-per-week'));
}
