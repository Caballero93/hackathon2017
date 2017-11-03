/**
   @author
   Predrag Nikolic

   @author
   Novak Boskov

   @author
   Alen Suljkanovic

   @copyright
   Typhoon HIL Inc.

   @license
   MIT
*/

SERVER_ADDRESS = "http://localhost";
SERVER_PORT = 8000;
refreshRate = 0.01;
/**
 * GET solution's results from the server
 */

function getResults() {
    $.ajax({
        url: SERVER_ADDRESS + ":" + SERVER_PORT + "/results",
        type: 'GET',
        success: data => {
            console.log("Data is here.");
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
var overall_output;

function vizResults(data) {
    var scale = 100;

    var price = data[data.length - 1].overall;
    $("#totalcost").html(Math.round(price * 100)/100);

    var cost = data[data.length - 1].overall_energy;
    $("#energycost").html(Math.round(cost * 100)/100);

    // Penalties
    var penalty_cost = 0;
    var penalty_num = 0;

//    var avg_runtime = data[data.length - 1].DataMessage.grid_status
//    $("#avgruntime").html(avg_runtime);

    var grid_st = data[data.length - 1].DataMessage.grid_status
    $("#gridstatus").html(grid_st);

    // data for the graph 1
    var total_cost = []
    var total_performance = []

    // data for the graph 2
    var real_load =[];
    var pv_power = [];
    var bess_power = [];
    var main_grid_power = [];
    var grid_status = [];
    var bess_soc = [];

    for(var i = 0; i < data.length; i++){
        // Calculate penalty data
        var curr = data[i];
        penalty_cost += curr.penal;

        if(curr.penal > 0){
            penalty_num += 1;
        }

        // Set graph data
        total_cost.push(curr.overall);
        total_performance.push(curr.performance);

        real_load.push(curr.real_load);
        pv_power.push(curr.pv_power);
        bess_power.push(curr.bess_power);
        grid_status.push(curr.DataMessage.grid_status);
        bess_soc.push(curr.bess_soc);

    }

    // Update penalty info on the HTML
    $("#penaltycost").html(Math.round(penalty_cost * 100)/100);
    $("#panaltycounter").html(penalty_num.length);

    // plots for the graph 1
    var cp_cost = {
      //x: x_size,
      y: total_cost,
      name: 'Total Cost',
      type: 'scatter'
    };

    var cp_perf = {
      //x: x_size,
      y: total_performance,
      name: 'Performance',
      yaxis: 'y2',
      type: 'scatter'
    };

    // plots for the graph 2
    var cp_real_load = {
      //x: x_size,
      y: real_load,
      name: 'Real Load',
      type: 'scatter'
    };

    var cp_pv_power = {
      //x: x_size,
      y: pv_power,
      name: 'PV Power',
      type: 'scatter'
    };

    var cp_bess_power = {
      //x: x_size,
      y: bess_power,
      name: 'Bess Power',
      type: 'scatter'
    };

    var cp_main_grid_power = {
      //x: x_size,
      y: main_grid_power,
      name: 'Main Grid Power',
      type: 'scatter'
    };

    var cp_grid_status = {
      //x: x_size,
      y: grid_status,
      name: 'Grid Status',
      yaxis: 'y2',
      type: 'scatter'
    };

    var cp_bess_soc = {
      //x: x_size,
      y: bess_soc,
      name: 'Bess SOC',
      yaxis: 'y2',
      type: 'scatter'
    };

    var g1_plot_data = [cp_cost, cp_perf];
    var g2_plot_data = [cp_bess_power, cp_main_grid_power, cp_real_load, cp_pv_power, cp_grid_status, cp_bess_soc];

    var cp_layout = {
      //title: 'Double Y Axis Example',
      //yaxis: {title: 'yaxis title'},
      yaxis2: {
        //title: 'yaxis2 title',
        titlefont: {color: 'rgb(148, 103, 189)'},
        tickfont: {color: 'rgb(148, 103, 189)'},
        overlaying: 'y',
        side: 'right'
      }
    };

    Plotly.newPlot('graph_1', g1_plot_data, cp_layout);
    Plotly.newPlot('graph_2', g2_plot_data, cp_layout);

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

/*
function myViewModel() {
        self.levelRead = ko.observable();
        self.levelData = ko.computed(function () {
            return self.levelRead();
        });
        getResults();
        self.levelRead(overall_output);
        alert(overall_output);
}

ko.applyBindings(new myViewModel());
*/
