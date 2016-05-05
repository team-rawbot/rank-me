import $ from 'jquery';

export function initForm() {
    if (document.body.classList.contains('page--competition-form')) {
        $('#id_players').select2();
    }
}
