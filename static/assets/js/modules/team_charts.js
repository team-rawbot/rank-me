define(["jquery", "underscore", "d3"], function ($, _, d3) {
    var TeamChart = function() {
        function head2head(container) {
            if(container.length == 0) {
                return;
            }

            var data = [];
            container.find('tbody tr').each(function () {
                var user = $(this).find('td:nth-child(1)').text();
                var wins = parseInt($(this).find('td:nth-child(2)').text());
                var defeats = parseInt($(this).find('td:nth-child(3)').text());
                var total = wins + defeats;

                data.push({
                    name: user,
                    values: [
                        { name: 'wins', value: wins / total, previous: 0 },
                        { name: 'defeats', value: defeats / total, previous: wins/total },
                        { name: 'total', value: total, previous: 0 }
                    ]
                });
            });

            var maxTotal = d3.max(data, function(d) { return d.values[2].value; });
            data.map(function(d) {d.values[2].value /= maxTotal; });

            container = container.parent();
            container.empty();

            var margin = {top: 20, right: 15, bottom: 30, left: 140},
                width = container.width() - margin.left - margin.right,
                height = 600;

            var x = d3.scale.linear()
                .rangeRound([0, width]);

            var y = d3.scale.ordinal()
                .rangeRoundBands([0, height], .1);

            var color = d3.scale.ordinal()
                .range(["#00ff00", "#ff0000", "#000000"])
                .domain(['wins', 'defeats', 'total']);

            var svg = d3.select(container[0]).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var names = data.map(function(d) { return d.name; });
            y.domain(names);

            var opponent = svg.selectAll(".opponent")
                .data(data)
              .enter()
                .append("g")
                .attr("class", "opponent")
                .attr("transform", function (d) {
                    return "translate(0, " + y(d.name) + ")";
                });

            opponent.selectAll("rect")
                .data(function (d) {
                    return d.values;
                })
              .enter()
                .append("rect")
                .attr("height", y.rangeBand() / 2)
                .attr('y', function(d) { return d.name == 'total' ? y.rangeBand() / 2 : 0; })
                .attr('x', function(d) { return x(d.previous); })
                .attr("width", function (d) { return x(d.value); })
                .style("fill", function (d) { return color(d.name); });

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .tickFormat(d3.format(".0%"));

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);
        }

        function drawChart() {
            head2head($('#head-2-head-results'));
        }

        return {
            drawChart: drawChart
        };
    }();

    return TeamChart;
});
