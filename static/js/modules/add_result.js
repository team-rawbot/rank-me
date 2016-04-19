import $ from 'jquery';

var alreadySelected = false;
var selects = '#add-result select';

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
function selectAs(field, event) {
    var option = $('#id_' + field + ' option[value=' + appDatas.user_id + ']');

    if(option && !alreadySelected) {
        option.attr('selected', 'selected');
        option.trigger('change');

        opposite(field).focus();
        alreadySelected = true;
        event.preventDefault();
    }
}

function removeUserFrom(user, field) {
    field.find('option').show();
    field.find('option[value=' + user + ']').hide();
}

export function init() {
    // focus "add result" button on load
    $('body.home #add-result-button').focus();

    $(selects).on('change', function() {
        removeUserFrom($(this).val(), opposite($(this).attr('id')));
    });

    $('#id_winner').select2();
    $('#id_loser').select2();

    $('body.page--add-result').keydown(function(event) {
        var username = appDatas.username;

        // press 'w' to set yourself as winner
        if (event.keyCode == 87) {
            selectAs('winner', event);
        }
        // press 'l' to set yourself as loser
        else if (event.keyCode == 76) {
            selectAs('loser', event);
        }
        // press Ctrl + enter to submit the form
        else if (event.keyCode == 13 && event.ctrlKey) {
            $('#add-result').submit();
        }
    });
}
