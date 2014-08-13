define(['jquery'], function($) {
    var alreadySelected = false;

    /**
     * return the opposite of field (winner if loser and vice versa)
     * @param field
     * @returns {*|jQuery|HTMLElement}
     */
    function opposite(field) {
        var opposite = '#id_loser';
        if (field == 'loser' || field == 'id_loser') {
            opposite = '#id_winner';
        }
        return $(opposite);
    }

    /**
     * Select the current user in the given field
     * @param field
     */
    function selectAs(field) {
        var option = $('#id_' + field + ' option:contains("' + appDatas.username + '")');

        if(option && !alreadySelected) {
            option.attr('selected', 'selected');

            opposite(field).focus();
            alreadySelected = true;
        }
    }

    var init = function() {
        // focus "add result" button on load
        $('body.home #add-result-button').focus();

        $('body.add-result').keydown(function(event) {
            var username = appDatas.username;

            // press 'w' to set yourself as winner
            if (event.keyCode == 87) {
                selectAs('winner');
            }
            // press 'l' to set yourself as loser
            else if (event.keyCode == 76) {
                selectAs('loser');
            }
        });
    };

    return {
        init: init
    };
});
