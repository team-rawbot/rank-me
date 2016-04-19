import $ from 'jquery';
import dropdown from 'bootstrap-sass/assets/javascripts/bootstrap/dropdown';
import select2 from 'select2';

import * as AddResult from 'modules/add_result';
import * as TeamChart from 'modules/team_charts';
import * as ScoreChart from 'modules/score_chart';
import UI from 'modules/UI';

$(function() {
    AddResult.init();
    TeamChart.drawChart();
    ScoreChart.drawChart($('#score-chart-container'));

    new UI();
});
