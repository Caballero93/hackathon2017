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
    if (stop) {
        window.location.search = 'refreshRate=Infinity';
    } else if (set) {
        window.location.search = 'refreshRate=' + $('#refreshRate').val();
    }
}

function vizResults() {
    var results = c3.generate({
        bindto: '#results',
        data: {
            columns: [
                ['data1', -30, 200, 200, 400, -150, 250],
                ['data2', 130, 100, -100, 200, -150, 50],
                ['data3', -230, 200, 200, -300, 250, 250],
                ['data4', -210, 80, 100, -40, 43, 99]
            ],
            type: 'bar',
            groups: [
                ['data1', 'data2', 'data3', 'data4']
            ]
        },
        grid: {
            y: {
                lines: [{value:0}]
            }
        }
    });
}

/**
 * Runs on <body onload>
 */
function vizOnLoad() {
    setPageRefresh();
    vizResults();

    // Refresh after number of seconds written in query parameter
    var qRefresh = window.location.search.split('=')[1] || 1;
    $('#refreshRate').val(qRefresh);
    if (qRefresh != Infinity) {
        setTimeout(function() {window.location = window.location;},
                   parseInt(qRefresh) * 1000);
    }
}
