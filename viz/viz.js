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
        success: data => vizResults(data),
        error: e =>
            console.log("Typhoon's framework server responded with an error."
                        + e)
    });
}

/**
 * Set page refresh rate from refresh rate input if set or stop refreshing.
 * @param {Bool} stop - stop refreshing
 * @param {Bool} set - set refresh rate using refresh rate input field
 */
function setPageRefresh(stopSet) {
    if (stopSet == "stop") {
        window.location.search = 'refreshRate=Infinity';
    } else if (stopSet == "set") {
        window.location.search = 'refreshRate=' + $('#refreshRate').val();
    }
}

/**
 * Draw barchart that represents solution's results
 * @param data - json that contains all results sent by the server
 */
function vizResults(data) {
    var scale = 100;
    var results = c3.generate({
        bindto: '#results',
        data: {
            columns: [
                ['energy efficiency'].concat(
                    data.map(x => x.energyMark * scale)),
                ['performance'].concat(
                    data.map(x => x.timeSpent * scale))
            ],
            type: 'bar',
            groups: [
                ['energy efficiency', 'performance']
            ],
            colors: {
                'energy efficiency': '#c43131',
                'performance': '#c4b8b8'
            }
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
    getResultsJSON();

    $('#refreshRateForm').submit(event => {
        event.preventDefault();
        setPageRefresh("set");
    });

    // Refresh after number of seconds written in query parameter
    var qRefresh = window.location.search.split('=')[1] || 1;
    $('#refreshRate').val(qRefresh);
    if (qRefresh != Infinity) {
        setTimeout(() =>  window.location = window.location,
                   parseInt(qRefresh) * 1000);
    }
}
