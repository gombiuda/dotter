$(function() {
    function update() {
	$.getJSON('/data', function(data) {
	    for (var i = 0; i < data.length; i++) {
		data[i][0] = (data[i][0] + 3600 * 8) * 1000;
	    }
	    $.plot("#placeholder", [ data ], {
		series: {
		    shadowSize: 0
		},
		yaxis: {
		    min: 0
		},
		xaxis: {
		    mode: "time",
		    minTickSize: [1, "second"],
		    timeformat: "%H:%M:%S"
		}
	    });
	    setTimeout(update, 1000);
	});
    }
    update();
});
