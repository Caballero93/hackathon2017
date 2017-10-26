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
refreshRate = 1;

/**
 * GET solution's results from the server
 */
function getResults() {
    $.ajax({
        url: SERVER_ADDRESS + ":" + SERVER_PORT + "/results",
        type: 'GET',
        success: data => {
            if (refreshRate != Infinity) {
                // visualize results after refreshRate seconds
                setTimeout(() => {

                    vizResults(data);

                    // Show refresh indicator once at 90% of
                    // refreshRate time
                    $('#refreshIndicator').html('Refreshing...');
                    setTimeout(() => $('#refreshIndicator').html('')
                               , 0.9 * refreshRate * 1000);

                    // recur to next cycle
                    getResults();
                }, refreshRate * 1000);
            }
        },
        error: e => {
            console.log("Typhoon's framework server responded with an error."
                        + e);
            if (refreshRate != Infinity) {
                setTimeout(() => getResults(), refreshRate);
            }
        }
    });
}

/**
 * Set page refresh rate from refresh rate input if set or stop refreshing.
 * @param {Bool} stop - stop refreshing
 * @param {Bool} set - set refresh rate using refresh rate input field
 */
function setPageRefresh(stopSet) {
    if (stopSet == "stop") {
        refreshRate = Infinity;
        $('#refreshRate').val(refreshRate);
        $('#refreshIndicator').html('');
    } else if (stopSet == "set") {
        refreshRate = parseInt($('#refreshRate').val());
        getResults();
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
    $('#refreshRateForm').submit(event => {
        event.preventDefault();
        setPageRefresh("set");
    });

    getResults();
}
