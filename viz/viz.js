/**
   @author
   Novak Boskov

   @copyright
   Typhoon HIL Inc.

   @license
   MIT
*/

SERVER_ADDRESS = "http://localhost";
SERVER_PORT = 8000;

function getResultsJSON() {
    $.ajax({
        url: SERVER_ADDRESS + ":" + SERVER_PORT + "/results",
        type: 'GET',
        success: function(data) { alert(data); },
        error: function() {
            console.log("Typhoon's framework server respond with error");
        }
    });
}

/**
 * Set page refresh rate from refresh rate input if set or stop refreshing.
 * @param {Bool} stop - stop refreshing
 * @param {Bool} set - set refresh rate using refresh rate input field
 */
function setPageRefresh(stop=false, set=false) {
    qRefresh = window.location.search.split('=')[1];
    if (qRefresh === undefined) {
        qRefresh = 1;
    }

    metaRefresh = $('head')
        .append('<meta http-equiv="refresh" content="' + qRefresh + '">');

    if (stop) {
        window.location.search = 'refreshRate=false';
    } else if (set) {
        window.location.search = 'refreshRate=' + $('#refreshRate').val();
    }
}

function vizResults() {
    var results = c3.generate({
        bindto: '#results',
        data: {
            columns: [
                ['data1', 30, 200, 100, 400, 150, 250],
                ['data2', 50, 20, 10, 40, 15, 25]
            ]
        }
    });
}

/**
 * Runs on <body onload>
 */
function vizOnLoad() {
    setPageRefresh();
    $('#refreshRate').val(parseInt(window.location.search.split('=')[1]));
    vizResults();
}
