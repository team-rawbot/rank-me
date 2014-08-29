define(["jquery", "underscore", "d3"], function($, _, d3) {
    var ScoreChart = function () {
        var modeSelector = 'input[name="score-chart-mode"]';

        function drawChart(container) {
            if(container.length == 0) {
                return;
            }

            d3.json(container.data('json'), function(err, data) {
                if(err) {
                    alert(err);
                    return;
                }

                var margin = { top: 20, right: 150, bottom: 40, left: 30 };
                var width = container.width() - margin.left - margin.right;
                var height = 400;

                var attribute = $(modeSelector + ':checked').val();
                container.empty();

                var color = d3.scale.category20();

                var x = d3.scale.linear()
                    .range([0, width]);
                var y = d3.scale.linear()
                    .range([0, height]);

                var line = d3.svg.line()
                    .interpolate("linear")
                    .x(function(d, idx) { return x(idx + 1); })
                    .y(function(d) { return y(d[attribute]); });

                var svg = d3.select(container[0])
                    .append('svg')
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                  .append('g')
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                color.domain(d3.keys(data));

                for(var name in data) {
                    if(data.hasOwnProperty(name)) {
                        data[name].map(function(d) {
                            d.name = name;
                            return d;
                        });
                    }
                }

                var positions = color.domain().map(function(name) {
                    return {
                        name: name,
                        values: data[name]
                    };
                });

                x.domain([1, positions[0].values.length]);

                var bigger = d3.max(positions, function(p) { return d3.max(p.values, function(v) { return v[attribute]; })});
                var smaller = d3.min(positions, function(p) { return d3.min(p.values, function(v) { return v[attribute]; })});

                if(attribute === 'position') {
                    y.domain([smaller, bigger]);
                } else {
                    y.domain([bigger, smaller]);
                }

                var position = svg.selectAll('.position')
                    .data(positions)
                  .enter()
                    .append('g')
                    .attr('class', 'position');

                position.append('path')
                    .attr('d', function(d) { return line(d.values); })
                    .attr('class', 'line')
                    .style("stroke", function (d) { return color(d.name); });

                position.selectAll('circle')
                    .data(function(d) { return d.values; })
                  .enter()
                    .append('circle')
                    .attr('r', function(d) { return d.played ? 4 : 0; })
                    .style('fill', function(d) { return d.win ? color(d.name) : 'white'; })
                    .style('stroke', function(d) { return color(d.name); })
                    .attr("transform", function(d, idx) { return "translate(" + x(idx + 1) + "," + y(d[attribute]) + ")"; });

                position.append("text")
                    .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
                    .attr("transform", function(d) { return "translate(" + x(50) + "," + y(d.value[attribute]) + ")"; })
                    .attr("x", 5)
                    .attr("dy", ".35em")
                    .style('stroke', function(d) { return color(d.name); })
                    .text(function(d) { return d.name; });

                var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient('bottom');
                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient('left');

                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + (height + 10) + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis);

            });
        }

        return {
            modeSelector: modeSelector,
            drawChart: drawChart
        };
    }();

    return ScoreChart;
});
