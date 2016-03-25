import $ from 'jquery';
import dropdown from 'bootstrap-sass/assets/javascripts/bootstrap/dropdown';

import * as AddResult from 'modules/add_result';
import * as TeamChart from 'modules/team_charts';
import * as ScoreChart from 'modules/score_chart';

$(function() {
    AddResult.init();
    TeamChart.drawChart();
    ScoreChart.drawChart($('#score-chart-container'));
});
