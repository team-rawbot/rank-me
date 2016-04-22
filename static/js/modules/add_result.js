import $ from 'jquery';

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

    if (option.length) {
        option.prop('selected', true);
        option.trigger('change');

        opposite(field).data('select2').open();
        event.preventDefault();
        discardShortcut();
    }
}

function discardShortcut() {
    $('.page--add-result').off('keydown.shortcut');
}

function removeUserFrom(user, field) {
    field.find('option').show();
    field.find('option[value=' + user + ']').hide();
}

export function init() {
    // focus "add result" button on load
    $('.page--competition #add-result-button').focus();

    $(selects).on('change', function() {
        removeUserFrom($(this).val(), opposite($(this).attr('id')));
    });

    $('#id_winner, #id_loser')
        .on('select2:opening', discardShortcut)
        .select2({
            placeholder: 'Select…',
            language: {
                'noResults': function() {
                    return 'No results found ☹️';
                }
            }
        });

    $('.page--add-result').on('keydown.shortcut', function(event) {
        // press 'w' to set yourself as winner
        if (event.keyCode == 87) {
            selectAs('winner', event);
        }
        // press 'l' to set yourself as loser
        else if (event.keyCode == 76) {
            selectAs('loser', event);
        }
        // press Ctrl/Cmd + enter to submit the form
        else if (event.KeyCode == 13 && (event.ctrlKey || event.metaKey)) {
            $('#add-result').submit();
        }
    });
}
