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
    var results = c3.generate({
        bindto: '#results',
        data: {
            columns: [
                ['Total cost'].concat(
                    data.map(x => x.overall * scale))/*,
                ['performance'].concat(
                    data.map(x => x.performance * scale))*/
            ],
            groups: [
                ['Total cost']
            ],
            colors: {
                'Total cost': '#c43131'
            }
        },
        subchart: {
            show: true
        }
    });
       var results2 = c3.generate({
        bindto: '#results2',
        data: {
            columns: [
                ['ESS power'].concat(
                    data.map(x => x.bessPower * scale)),
                ['Load power'].concat(
                    data.map(x => x.DataMessage.current_load * scale)),
                ['Grid power'].concat(
                    data.map(x => x.mainGridPower * scale))
            ],
            groups: [
                ['energy efficiency', 'performance']
            ],
            colors: {
                'energy efficiency': '#c43131',
                'performance': '#c4b8b8'
            },
            axes: {
                data1: 'y',
                data2: 'y2'
            }
        },
        subchart: {
            show: true
        },axis: {
            y2: {
                show: true
            }
        }
    });
	
	var power1GaugeContainer1 = c3.generate({
        bindto: '#power1GaugeContainer',
        data: {
            columns: [
                    ['Grid Power',(data[data.length-1].DataMessage.mainGridPower).toFixed(2)]
                ],
                type: 'gauge'
                },
                gauge: {
                    label: {
                        format: function(value, ratio) {
                            return value;
                        },
                        show: true // to turn off the min/max labels.
                    },
                    min: -1000, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
                    max: 1000, // 100 is default
                    units: ' mainGridPower (W)',
                    width: 39 // for adjusting arc thickness
                },
                color: {
                    pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
                    threshold: {
                        unit: ' W', // percentage is default
                        max: 100, // 100 is default
                        values: [30, 60, 90, 100]
                    }
                },
                size: {
                    height: 180
                }
    });
    var power1GaugeContainer2 = c3.generate({
        bindto: '#power2GaugeContainer',
        data: {
            columns: [
                    ['ESS power',(data[data.length-1].bessPower).toFixed(2)]
                ],
                type: 'gauge'
                },
                gauge: {
                    label: {
                        format: function(value, ratio) {
                            return value;
                        },
                        show: true // to turn off the min/max labels.
                    },
                    min: -1000, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
                    max: 1000, // 100 is default
                    units: ' bessPower',
                    width: 39 // for adjusting arc thickness
                },
                color: {
                    pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
                    threshold: {
                        unit: ' W', // percentage is default
                        max: 100, // 100 is default
                        values: [30, 60, 90, 100]
                    }
                },
                size: {
                    height: 180
                }
    });
    var power1GaugeContainer3 = c3.generate({
        bindto: '#power3GaugeContainer',
        data: {
            columns: [
                    ['PV',(data[data.length-1].DataMessage.solar_production).toFixed(2)]
                ],
                type: 'gauge'
                },
                gauge: {
                    label: {
                        format: function(value, ratio) {
                            return value;
                        },
                        show: true // to turn off the min/max labels.
                    },
                    min: -1000, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
                    max: 1000, // 100 is default
                    units: ' solar_production',
                    width: 39 // for adjusting arc thickness
                },
                color: {
                    pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
                    threshold: {
                        unit: ' W', // percentage is default
                        max: 100, // 100 is default
                        values: [30, 60, 90, 100]
                    }
                },
                size: {
                    height: 180
                }
    });
    var power1GaugeContainer4 = c3.generate({
        bindto: '#power4GaugeContainer',
        data: {
            columns: [
                    ['Load Power',(data[data.length-1].DataMessage.current_load).toFixed(2)]
                ],
                type: 'gauge'
                },
                gauge: {
                    label: {
                        format: function(value, ratio) {
                            return value;
                        },
                        show: true // to turn off the min/max labels.
                    },
                    min: -1000, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
                    max: 1000, // 100 is default
                    units: ' current_Load',
                    width: 39 // for adjusting arc thickness
                },
                color: {
                    pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
                    threshold: {
                        unit: ' W', // percentage is default
                        max: 100, // 100 is default
                        values: [30, 60, 90, 100]
                    }
                },
                size: {
                    height: 180
                }
    });
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


/*!
 * @license Open source under BSD 2-clause (http://choosealicense.com/licenses/bsd-2-clause/)
 * Copyright (c) 2015, Curtis Bratton
 * All rights reserved.
 *
 * Liquid Fill Gauge v1.1
 */
function liquidFillGaugeDefaultSettings(){
    return {
        minValue: 0, // The gauge minimum value.
        maxValue: 100, // The gauge maximum value.
        circleThickness: 0.05, // The outer circle thickness as a percentage of it's radius.
        circleFillGap: 0.05, // The size of the gap between the outer circle and wave circle as a percentage of the outer circles radius.
        circleColor: "#178BCA", // The color of the outer circle.
        waveHeight: 0, // The wave height as a percentage of the radius of the wave circle.
        waveCount: 1, // The number of full waves per width of the wave circle.
        waveRiseTime: 1000, // The amount of time in milliseconds for the wave to rise from 0 to it's final height.
        waveAnimateTime: 18000, // The amount of time in milliseconds for a full wave to enter the wave circle.
        waveRise: true, // Control if the wave should rise from 0 to it's full height, or start at it's full height.
        waveHeightScaling: true, // Controls wave size scaling at low and high fill percentages. When true, wave height reaches it's maximum at 50% fill, and minimum at 0% and 100% fill. This helps to prevent the wave from making the wave circle from appear totally full or empty when near it's minimum or maximum fill.
        waveAnimate: false, // Controls if the wave scrolls or is static.
        waveColor: "#5e91cc", // The color of the fill wave.
        waveOffset: 0, // The amount to initially offset the wave. 0 = no offset. 1 = offset of one full wave.
        textVertPosition: .5, // The height at which to display the percentage text withing the wave circle. 0 = bottom, 1 = top.
        textSize: 1, // The relative height of the text to display in the wave circle. 1 = 50%
        valueCountUp: true, // If true, the displayed value counts up from 0 to it's final value upon loading. If false, the final value is displayed.
        displayPercent: true, // If true, a % symbol is displayed after the value.
        textColor: "#045681", // The color of the value text when the wave does not overlap it.
        waveTextColor: "#A4DBf8" // The color of the value text when the wave overlaps it.
    };
}

function loadLiquidFillGauge(elementId, value, config) {
    if(config == null) config = liquidFillGaugeDefaultSettings();

    var gauge = d3.select("#" + elementId);
    var radius = Math.min(parseInt(gauge.style("width")), parseInt(gauge.style("height")))/2;
    var locationX = parseInt(gauge.style("width"))/2 - radius;
    var locationY = parseInt(gauge.style("height"))/2 - radius;
    var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value))/config.maxValue;

    var waveHeightScale;
    if(config.waveHeightScaling){
        waveHeightScale = d3.scale.linear()
            .range([0,config.waveHeight,0])
            .domain([0,50,100]);
    } else {
        waveHeightScale = d3.scale.linear()
            .range([config.waveHeight,config.waveHeight])
            .domain([0,100]);
    }

    var textPixels = (config.textSize*radius/2);
    var textFinalValue = parseFloat(value).toFixed(2);
    var textStartValue = config.valueCountUp?config.minValue:textFinalValue;
    var percentText = config.displayPercent?"%":"";
    var circleThickness = config.circleThickness * radius;
    var circleFillGap = config.circleFillGap * radius;
    var fillCircleMargin = circleThickness + circleFillGap;
    var fillCircleRadius = radius - fillCircleMargin;
    var waveHeight = fillCircleRadius*waveHeightScale(fillPercent*100);

    var waveLength = fillCircleRadius*2/config.waveCount;
    var waveClipCount = 1+config.waveCount;
    var waveClipWidth = waveLength*waveClipCount;

    // Rounding functions so that the correct number of decimal places is always displayed as the value counts up.
    var textRounder = function(value){ return Math.round(value); };
    if(parseFloat(textFinalValue) != parseFloat(textRounder(textFinalValue))){
        textRounder = function(value){ return parseFloat(value).toFixed(1); };
    }
    if(parseFloat(textFinalValue) != parseFloat(textRounder(textFinalValue))){
        textRounder = function(value){ return parseFloat(value).toFixed(2); };
    }

    // Data for building the clip wave area.
    var data = [];
    for(var i = 0; i <= 40*waveClipCount; i++){
        data.push({x: i/(40*waveClipCount), y: (i/(40))});
    }

    // Scales for drawing the outer circle.
    var gaugeCircleX = d3.scale.linear().range([0,2*Math.PI]).domain([0,1]);
    var gaugeCircleY = d3.scale.linear().range([0,radius]).domain([0,radius]);

    // Scales for controlling the size of the clipping path.
    var waveScaleX = d3.scale.linear().range([0,waveClipWidth]).domain([0,1]);
    var waveScaleY = d3.scale.linear().range([0,waveHeight]).domain([0,1]);

    // Scales for controlling the position of the clipping path.
    var waveRiseScale = d3.scale.linear()
        // The clipping area size is the height of the fill circle + the wave height, so we position the clip wave
        // such that the it will overlap the fill circle at all when at 0%, and will totally cover the fill
        // circle at 100%.
        .range([(fillCircleMargin+fillCircleRadius*2+waveHeight),(fillCircleMargin-waveHeight)])
        .domain([0,1]);
    var waveAnimateScale = d3.scale.linear()
        .range([0, waveClipWidth-fillCircleRadius*2]) // Push the clip area one full wave then snap back.
        .domain([0,1]);

    // Scale for controlling the position of the text within the gauge.
    var textRiseScaleY = d3.scale.linear()
        .range([fillCircleMargin+fillCircleRadius*2,(fillCircleMargin+textPixels*0.7)])
        .domain([0,1]);

    // Center the gauge within the parent SVG.
    var gaugeGroup = gauge.append("g")
        .attr('transform','translate('+locationX+','+locationY+')');

    // Draw the outer circle.
    var gaugeCircleArc = d3.svg.arc()
        .startAngle(gaugeCircleX(0))
        .endAngle(gaugeCircleX(1))
        .outerRadius(gaugeCircleY(radius))
        .innerRadius(gaugeCircleY(radius-circleThickness));
    gaugeGroup.append("path")
        .attr("d", gaugeCircleArc)
        .style("fill", config.circleColor)
        .attr('transform','translate('+radius+','+radius+')');

    // Text where the wave does not overlap.
    var text1 = gaugeGroup.append("text")
        .text(textRounder(textStartValue) + percentText)
        .attr("class", "liquidFillGaugeText")
        .attr("text-anchor", "middle")
        .attr("font-size", textPixels + "px")
        .style("fill", config.textColor)
        .attr('transform','translate('+radius+','+textRiseScaleY(config.textVertPosition)+')');

    // The clipping wave area.
    var clipArea = d3.svg.area()
        .x(function(d) { return waveScaleX(d.x); } )
        .y0(function(d) { return waveScaleY(Math.sin(Math.PI*2*config.waveOffset*-1 + Math.PI*2*(1-config.waveCount) + d.y*2*Math.PI));} )
        .y1(function(d) { return (fillCircleRadius*2 + waveHeight); } );
    var waveGroup = gaugeGroup.append("defs")
        .append("clipPath")
        .attr("id", "clipWave" + elementId);
    var wave = waveGroup.append("path")
        .datum(data)
        .attr("d", clipArea)
        .attr("T", 0);

    // The inner circle with the clipping wave attached.
    var fillCircleGroup = gaugeGroup.append("g")
        .attr("clip-path", "url(#clipWave" + elementId + ")");
    fillCircleGroup.append("circle")
        .attr("cx", radius)
        .attr("cy", radius)
        .attr("r", fillCircleRadius)
        .style("fill", config.waveColor);

    // Text where the wave does overlap.
    var text2 = fillCircleGroup.append("text")
        .text(textRounder(textStartValue) + percentText)
        .attr("class", "liquidFillGaugeText")
        .attr("text-anchor", "middle")
        .attr("font-size", textPixels + "px")
        .style("fill", config.waveTextColor)
        .attr('transform','translate('+radius+','+textRiseScaleY(config.textVertPosition)+')');

    // Make the value count up.
    if(config.valueCountUp){
        var textTween = function(){
            var i = d3.interpolate(this.textContent, textFinalValue);
            return function(t) { this.textContent = textRounder(i(t)) + percentText; }
        };
        text1.transition()
            .duration(config.waveRiseTime)
            .tween("text", textTween);
        text2.transition()
            .duration(config.waveRiseTime)
            .tween("text", textTween);
    }

    // Make the wave rise. wave and waveGroup are separate so that horizontal and vertical movement can be controlled independently.
    var waveGroupXPosition = fillCircleMargin+fillCircleRadius*2-waveClipWidth;
    if(config.waveRise){
        waveGroup.attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(0)+')')
            .transition()
            .duration(config.waveRiseTime)
            .attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(fillPercent)+')')
            .each("start", function(){ wave.attr('transform','translate(1,0)'); }); // This transform is necessary to get the clip wave positioned correctly when waveRise=true and waveAnimate=false. The wave will not position correctly without this, but it's not clear why this is actually necessary.
    } else {
        waveGroup.attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(fillPercent)+')');
    }

    if(config.waveAnimate) animateWave();

    function animateWave() {
        wave.attr('transform','translate('+waveAnimateScale(wave.attr('T'))+',0)');
        wave.transition()
            .duration(config.waveAnimateTime * (1-wave.attr('T')))
            .ease('linear')
            .attr('transform','translate('+waveAnimateScale(1)+',0)')
            .attr('T', 1)
            .each('end', function(){
                wave.attr('T', 0);
                animateWave(config.waveAnimateTime);
            });
    }

    function GaugeUpdater(){
        this.update = function(value){
            var newFinalValue = parseFloat(value).toFixed(2);
            var textRounderUpdater = function(value){ return Math.round(value); };
            if(parseFloat(newFinalValue) != parseFloat(textRounderUpdater(newFinalValue))){
                textRounderUpdater = function(value){ return parseFloat(value).toFixed(1); };
            }
            if(parseFloat(newFinalValue) != parseFloat(textRounderUpdater(newFinalValue))){
                textRounderUpdater = function(value){ return parseFloat(value).toFixed(2); };
            }

            var textTween = function(){
                var i = d3.interpolate(this.textContent, parseFloat(value).toFixed(2));
                return function(t) { this.textContent = textRounderUpdater(i(t)) + percentText; }
            };

            text1.transition()
                .duration(config.waveRiseTime)
                .tween("text", textTween);
            text2.transition()
                .duration(config.waveRiseTime)
                .tween("text", textTween);

            var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value))/config.maxValue;
            var waveHeight = fillCircleRadius*waveHeightScale(fillPercent*100);
            var waveRiseScale = d3.scale.linear()
                // The clipping area size is the height of the fill circle + the wave height, so we position the clip wave
                // such that the it will overlap the fill circle at all when at 0%, and will totally cover the fill
                // circle at 100%.
                .range([(fillCircleMargin+fillCircleRadius*2+waveHeight),(fillCircleMargin-waveHeight)])
                .domain([0,1]);
            var newHeight = waveRiseScale(fillPercent);
            var waveScaleX = d3.scale.linear().range([0,waveClipWidth]).domain([0,1]);
            var waveScaleY = d3.scale.linear().range([0,waveHeight]).domain([0,1]);
            var newClipArea;
            if(config.waveHeightScaling){
                newClipArea = d3.svg.area()
                    .x(function(d) { return waveScaleX(d.x); } )
                    .y0(function(d) { return waveScaleY(Math.sin(Math.PI*2*config.waveOffset*-1 + Math.PI*2*(1-config.waveCount) + d.y*2*Math.PI));} )
                    .y1(function(d) { return (fillCircleRadius*2 + waveHeight); } );
            } else {
                newClipArea = clipArea;
            }

            var newWavePosition = config.waveAnimate?waveAnimateScale(1):0;
            wave.transition()
                .duration(0)
                .transition()
                .duration(config.waveAnimate?(config.waveAnimateTime * (1-wave.attr('T'))):(config.waveRiseTime))
                .ease('linear')
                .attr('d', newClipArea)
                .attr('transform','translate('+newWavePosition+',0)')
                .attr('T','1')
                .each("end", function(){
                    if(config.waveAnimate){
                        wave.attr('transform','translate('+waveAnimateScale(0)+',0)');
                        animateWave(config.waveAnimateTime);
                    }
                });
            waveGroup.transition()
                .duration(config.waveRiseTime)
                .attr('transform','translate('+waveGroupXPosition+','+newHeight+')')
        }
    }

    return new GaugeUpdater();
}

function Gauge(placeholderName, configuration)
{
	this.placeholderName = placeholderName;

	var self = this; // for internal d3 functions

	this.configure = function(configuration)
	{
		this.config = configuration;

		this.config.size = this.config.size * 0.9;

		this.config.raduis = this.config.size * 0.97 / 2;
		this.config.cx = this.config.size / 2;
		this.config.cy = this.config.size / 2;

		this.config.min = undefined != configuration.min ? configuration.min : 0;
		this.config.max = undefined != configuration.max ? configuration.max : 100;
		this.config.range = this.config.max - this.config.min;

		this.config.majorTicks = configuration.majorTicks || 5;
		this.config.minorTicks = configuration.minorTicks || 2;

		this.config.greenColor 	= configuration.greenColor || "#109618";
		this.config.yellowColor = configuration.yellowColor || "#FF9900";
		this.config.redColor 	= configuration.redColor || "#DC3912";

		this.config.transitionDuration = configuration.transitionDuration || 500;
	}

	this.render = function()
	{
		this.body = d3.select("#" + this.placeholderName)
							.append("svg:svg")
							.attr("class", "gauge")
							.attr("width", this.config.size)
							.attr("height", this.config.size);

		this.body.append("svg:circle")
					.attr("cx", this.config.cx)
					.attr("cy", this.config.cy)
					.attr("r", this.config.raduis)
					.style("fill", "#ccc")
					.style("stroke", "#000")
					.style("stroke-width", "0.5px");

		this.body.append("svg:circle")
					.attr("cx", this.config.cx)
					.attr("cy", this.config.cy)
					.attr("r", 0.9 * this.config.raduis)
					.style("fill", "#fff")
					.style("stroke", "#e0e0e0")
					.style("stroke-width", "2px");

		for (var index in this.config.greenZones)
		{
			this.drawBand(this.config.greenZones[index].from, this.config.greenZones[index].to, self.config.greenColor);
		}

		for (var index in this.config.yellowZones)
		{
			this.drawBand(this.config.yellowZones[index].from, this.config.yellowZones[index].to, self.config.yellowColor);
		}

		for (var index in this.config.redZones)
		{
			this.drawBand(this.config.redZones[index].from, this.config.redZones[index].to, self.config.redColor);
		}

		if (undefined != this.config.label)
		{
			var fontSize = Math.round(this.config.size / 9);
			this.body.append("svg:text")
						.attr("x", this.config.cx)
						.attr("y", this.config.cy / 2 + fontSize / 2)
						.attr("dy", fontSize / 2)
						.attr("text-anchor", "middle")
						.text(this.config.label)
						.style("font-size", fontSize + "px")
						.style("fill", "#333")
						.style("stroke-width", "0px");
		}

		var fontSize = Math.round(this.config.size / 16);
		var majorDelta = this.config.range / (this.config.majorTicks - 1);
		for (var major = this.config.min; major <= this.config.max; major += majorDelta)
		{
			var minorDelta = majorDelta / this.config.minorTicks;
			for (var minor = major + minorDelta; minor < Math.min(major + majorDelta, this.config.max); minor += minorDelta)
			{
				var point1 = this.valueToPoint(minor, 0.75);
				var point2 = this.valueToPoint(minor, 0.85);

				this.body.append("svg:line")
							.attr("x1", point1.x)
							.attr("y1", point1.y)
							.attr("x2", point2.x)
							.attr("y2", point2.y)
							.style("stroke", "#666")
							.style("stroke-width", "1px");
			}

			var point1 = this.valueToPoint(major, 0.7);
			var point2 = this.valueToPoint(major, 0.85);

			this.body.append("svg:line")
						.attr("x1", point1.x)
						.attr("y1", point1.y)
						.attr("x2", point2.x)
						.attr("y2", point2.y)
						.style("stroke", "#333")
						.style("stroke-width", "2px");

			if (major == this.config.min || major == this.config.max)
			{
				var point = this.valueToPoint(major, 0.63);

				this.body.append("svg:text")
				 			.attr("x", point.x)
				 			.attr("y", point.y)
				 			.attr("dy", fontSize / 3)
				 			.attr("text-anchor", major == this.config.min ? "start" : "end")
				 			.text(major)
				 			.style("font-size", fontSize + "px")
							.style("fill", "#333")
							.style("stroke-width", "0px");
			}
		}

		var pointerContainer = this.body.append("svg:g").attr("class", "pointerContainer");

		var midValue = (this.config.min + this.config.max) / 2;

		var pointerPath = this.buildPointerPath(midValue);

		var pointerLine = d3.svg.line()
									.x(function(d) { return d.x })
									.y(function(d) { return d.y })
									.interpolate("basis");

		pointerContainer.selectAll("path")
							.data([pointerPath])
							.enter()
								.append("svg:path")
									.attr("d", pointerLine)
									.style("fill", "#dc3912")
									.style("stroke", "#c63310")
									.style("fill-opacity", 0.7)

		pointerContainer.append("svg:circle")
							.attr("cx", this.config.cx)
							.attr("cy", this.config.cy)
							.attr("r", 0.12 * this.config.raduis)
							.style("fill", "#4684EE")
							.style("stroke", "#666")
							.style("opacity", 1);

		var fontSize = Math.round(this.config.size / 10);
		pointerContainer.selectAll("text")
							.data([midValue])
							.enter()
								.append("svg:text")
									.attr("x", this.config.cx)
									.attr("y", this.config.size - this.config.cy / 4 - fontSize)
									.attr("dy", fontSize / 2)
									.attr("text-anchor", "middle")
									.style("font-size", fontSize + "px")
									.style("fill", "#000")
									.style("stroke-width", "0px");

		this.redraw(this.config.min, 0);
	}

	this.buildPointerPath = function(value)
	{
		var delta = this.config.range / 13;

		var head = valueToPoint(value, 0.85);
		var head1 = valueToPoint(value - delta, 0.12);
		var head2 = valueToPoint(value + delta, 0.12);

		var tailValue = value - (this.config.range * (1/(270/360)) / 2);
		var tail = valueToPoint(tailValue, 0.28);
		var tail1 = valueToPoint(tailValue - delta, 0.12);
		var tail2 = valueToPoint(tailValue + delta, 0.12);

		return [head, head1, tail2, tail, tail1, head2, head];

		function valueToPoint(value, factor)
		{
			var point = self.valueToPoint(value, factor);
			point.x -= self.config.cx;
			point.y -= self.config.cy;
			return point;
		}
	}

	this.drawBand = function(start, end, color)
	{
		if (0 >= end - start) return;

		this.body.append("svg:path")
					.style("fill", color)
					.attr("d", d3.svg.arc()
						.startAngle(this.valueToRadians(start))
						.endAngle(this.valueToRadians(end))
						.innerRadius(0.65 * this.config.raduis)
						.outerRadius(0.85 * this.config.raduis))
					.attr("transform", function() { return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(270)" });
	}

	this.redraw = function(value, transitionDuration)
	{
		var pointerContainer = this.body.select(".pointerContainer");

		pointerContainer.selectAll("text").text(Math.round(value));

		var pointer = pointerContainer.selectAll("path");
		pointer.transition()
					.duration(undefined != transitionDuration ? transitionDuration : this.config.transitionDuration)
					//.delay(0)
					//.ease("linear")
					//.attr("transform", function(d)
					.attrTween("transform", function()
					{
						var pointerValue = value;
						if (value > self.config.max) pointerValue = self.config.max + 0.02*self.config.range;
						else if (value < self.config.min) pointerValue = self.config.min - 0.02*self.config.range;
						var targetRotation = (self.valueToDegrees(pointerValue) - 90);
						var currentRotation = self._currentRotation || targetRotation;
						self._currentRotation = targetRotation;

						return function(step)
						{
							var rotation = currentRotation + (targetRotation-currentRotation)*step;
							return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(" + rotation + ")";
						}
					});
	}

	this.valueToDegrees = function(value)
	{
		// thanks @closealert
		//return value / this.config.range * 270 - 45;
		return value / this.config.range * 270 - (this.config.min / this.config.range * 270 + 45);
	}

	this.valueToRadians = function(value)
	{
		return this.valueToDegrees(value) * Math.PI / 180;
	}

	this.valueToPoint = function(value, factor)
	{
		return { 	x: this.config.cx - this.config.raduis * factor * Math.cos(this.valueToRadians(value)),
					y: this.config.cy - this.config.raduis * factor * Math.sin(this.valueToRadians(value)) 		};
	}

	// initialization
	this.configure(configuration);
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

/* DRAW GAUGES */

 var gauges = [];

			function createGauge(name, label, min, max)
			{
				var config =
				{
					size: 200,
					label: label,
					min: undefined != min ? min : 0,
					max: undefined != max ? max : 100,
					minorTicks: 5
				}

				var range = config.max - config.min;
				config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
				config.redZones = [{ from: config.min + range*0.9, to: config.max }];

				gauges[name] = new Gauge(name + "GaugeContainer", config);
				gauges[name].render();
			}

			function createGauges()
			{
				createGauge("power1", "Grid power");
				createGauge("power2", "ESS power");
				createGauge("power3", "Load power");
				createGauge("power4", "ESS power");
			}

			function updateGauges()
			{
				for (var key in gauges)
				{
					var value = getRandomValue(gauges[key])
					gauges[key].redraw(value);
				}
			}

			function getRandomValue(gauge)
			{
				var overflow = 0; //10;
				return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow*2) *  Math.random();
			}

			function initialize()
			{
				createGauges();
				setInterval(updateGauges, 1000);
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
