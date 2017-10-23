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

var results = c3.generate({
    bindto: '#results',
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 50, 20, 10, 40, 15, 25]
        ]
    }
});
