define(["jquery", "underscore", "d3"], function($, _, d3) {
    var ScoreChart = function () {
        var modeSelector = 'input[name="score-chart-mode"]';

        var attribute;
        var positions;
        var x, y;

        function setDomain() {
            x.domain([1, positions[0].values.length]);

            var bigger = d3.max(positions, function(p) { return d3.max(p.values, function(v) { return v[attribute]; })});
            var smaller = d3.min(positions, function(p) { return d3.min(p.values, function(v) { return v[attribute]; })});

            if(attribute === 'position') {
                y.domain([smaller, bigger]);
            } else {
                y.domain([bigger, smaller]);
            }
        }

        function drawChart(container) {
            if(container.length == 0) {
                return;
            }

            d3.json(container.data('json'), function(err, data) {
                if(err) {
                    alert(err);
                    return;
                }

                var margin = { top: 20, right: 150, bottom: 10, left: 40 };
                var width = container.width() - margin.left - margin.right;
                var height = 400;

                attribute = $(modeSelector + ':checked').val();
                $(modeSelector).on('change', function() {
                    var t = svg.selectAll(".position").transition().duration(1250);

                    attribute = $(this).val();
                    setDomain();

                    // redraw relevent part of each item
                    t.select('path')
                        .attr('d', function(d) { return line(d.values); });

                    t.selectAll('circle')
                        .attr("transform", function(d, idx) { return "translate(" + x(idx + 1) + "," + y(d[attribute]) + ")"; });

                     svg.select('.y.axis').call(yAxis);
                });

                var color = d3.scale.category20();

                x = d3.scale.linear()
                    .range([0, width]);
                y = d3.scale.linear()
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

                positions = color.domain().map(function(name) {
                    return {
                        name: name,
                        values: data[name]
                    };
                });

                setDomain();

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
                    .attr('r', function(d) { return d.played ? 5 : 0; })
                    .style('fill', function(d) { return d.win ? color(d.name) : 'white'; })
                    .style('stroke', function(d) { return color(d.name); })
                    .attr("transform", function(d, idx) { return "translate(" + x(idx + 1) + "," + y(d[attribute]) + ")"; });

                position.append("text")
                    .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
                    .attr("transform", function(d) { return "translate(" + x(50) + "," + y(d.value[attribute]) + ")"; })
                    .attr("x", 10)
                    .attr("dy", ".35em")
                    .style('fill', function(d) { return color(d.name); })
                    .text(function(d) { return d.name; });

                var yAxis = d3.svg.axis()
                    .scale(y)
                    .ticks(20)
                    .tickSize(0)
                    .orient('left');

                svg.append("g")
                    .attr("class", "y axis")
                    .attr("transform", function(d, idx) { return "translate(-5, 0)"; })
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
