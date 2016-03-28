import $ from 'jquery';

export default class UI {

    constructor() {
        this.addMenuListeners();
    }

    addMenuListeners() {
        $('#sidebar-collapse-button').on('click', () => {
            $('#sidebar-collapse').slideToggle('fast');
        });
    }

}
