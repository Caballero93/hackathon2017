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
            console.log("Data is here.");
                vizResults(data);
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
                }, refreshRate * 1200);
            }
        },
        error: (_, __, error) => {
            console.log("Typhoon's framework server responded with an error.\n"
                        + error);

            if (refreshRate != Infinity) {
                setTimeout(() => getResults(), refreshRate * 1000);
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


    var trace1 = {
      x: [1,2,3,4],
      y: [5,6,7,8],
      mode: 'lines',
      name: 'Lines'
    };


var data = [trace1];

var layout = {
  title: 'Title of the Graph',
  xaxis: {
    title: 'x-axis title'
  },
  yaxis: {
    title: 'y-axis title'
  }
};

Plotly.newPlot('results', data, layout);
}

 /*   var overall_output = data[data.length-1].overall;
    console.log('overall ' + overall_output);
    console.log('energyMark ' + data[data.length-1].energyMark);
    console.log('performance ' + data[data.length-1].performance);
    console.log('bessSOC ' + data[data.length-1].bessSOC);
    console.log('bessOverload ' + data[data.length-1].bessOverload);
    console.log('bessPower ' + data[data.length-1].bessPower);
    console.log('mainGridPower ' + data[data.length-1].mainGridPower);
    console.log('penal ' + data[data.length-1].penal);
    console.log(' ');
    console.log('id ' + data[data.length-1].DataMessage.id);
    console.log('grid_status ' + data[data.length-1].DataMessage.grid_status);
    console.log('buying_price ' + data[data.length-1].DataMessage.buying_price);
    console.log('selling_price ' + data[data.length-1].DataMessage.selling_price);
    console.log('current_load ' + data[data.length-1].DataMessage.current_load);
    console.log('solar_production ' + data[data.length-1].DataMessage.solar_production);
    console.log('bessSOC ' + data[data.length-1].DataMessage.bessSOC);
    console.log('bessOverload ' + data[data.length-1].DataMessage.bessOverload);
    console.log('mainGridPower ' + data[data.length-1].DataMessage.mainGridPower);
    console.log(' ');
	*/


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

/* CLOCK */

var showD3Clock = function() {

  var w = 320             // Width of SVG element
  var h = 320             // Height of SVG element

  var cx = w / 2          // Center x
  var cy = h / 2          // Center y
  var margin = 4
  var r = w / 2 - margin  // Radius of clock face

  var svg = d3.select(".box.b .clock").append("svg")
    .attr("class", "clock")
    .attr("width", w)
    .attr("height", h)

  makeClockFace()

  // Create hands from dataset
  svg.selectAll("line.hand")
    .data(getTimeOfDay())
    .enter()
    .append("line")
    .attr("class", function (d) { return d[0] + " hand"})
    .attr("x1", cx)
    .attr("y1", function (d) { return cy + handBackLength(d) })
    .attr("x2", cx)
    .attr("y2", function (d) { return r - handLength(d)})
    .attr("transform", rotationTransform)

  // Update hand positions once per second
  setInterval(updateHands, 1000)

  function makeClockFace() {
    var hourTickLength = Math.round(r * 0.2)
    var minuteTickLength = Math.round(r * 0.075)
    for (var i = 0; i < 60; ++i) {
      var tickLength, tickClass
      if ((i % 5) == 0) {
        tickLength = hourTickLength
        tickClass = "hourtick"
      }
      else {
        tickLength = minuteTickLength
        tickClass = "minutetick"
      }
      svg.append("line")
        .attr("class", tickClass + " face")
        .attr("x1", cx)
        .attr("y1", margin)
        .attr("x2", cx)
        .attr("y2", margin + tickLength)
        .attr("transform", "rotate(" + i * 6 + "," + cx + "," + cy + ")")
    }
  }

  function getTimeOfDay() {
    var now = new Date()
    var hr = now.getHours()
    var min = now.getMinutes()
    var sec = now.getSeconds()
    return [
      [ "hour",   hr + (min / 60) + (sec / 3600) ],
      [ "minute", min + (sec / 60) ]/*,
      [ "second", sec ]*/
    ]
  }

  function handLength(d) {
    if (d[0] == "hour")
      return Math.round(0.45 * r)
    else
      return Math.round(0.90 * r)
  }

  function handBackLength(d) {
    if (d[0] == "second")
      return Math.round(0.25 * r)
    else
      return Math.round(0.10 * r)
  }

  function rotationTransform(d) {
    var angle
    if (d[0] == "hour")
      angle = (d[1] % 12) * 30
    else
      angle = d[1] * 6
    return "rotate(" + angle + "," + cx + "," + cy + ")"
  }

  function updateHands() {
    svg.selectAll("line.hand")
      .data(getTimeOfDay())
      .transition().ease("bounce")
      .attr("transform", rotationTransform)
  }
}

showD3Clock()
