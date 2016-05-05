import $ from 'jquery';
import 'bootstrap-sass/assets/javascripts/bootstrap/dropdown';
import 'select2';

import * as AddResult from 'modules/add_result';
import * as TeamChart from 'modules/team_charts';
import * as ScoreChart from 'modules/score_chart';
import * as Competitions from 'modules/competitions';
import UI from 'modules/UI';

$(function() {
    AddResult.init();
    TeamChart.drawChart();
    ScoreChart.drawChart($('#score-chart-container'));
    Competitions.initForm();
    new UI();
});
