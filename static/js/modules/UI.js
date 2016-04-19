import $ from 'jquery';

export default class UI {

    constructor() {
        this.addMenuListeners();
        this.preventClickOnDisabledLinks();
    }

    addMenuListeners() {
        $('#sidebar-collapse-button').on('click', () => {
            $('#sidebar-collapse').slideToggle('fast');
        });
    }

    preventClickOnDisabledLinks() {
        $('a[disabled]').on('click', (event) => {
            event.preventDefault();
        });
    }

}
