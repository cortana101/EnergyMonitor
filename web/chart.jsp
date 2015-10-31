<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<script src="js/jquery-2.1.4.min.js"></script>
<html>
<!-- 20 minute auto page refresh -->
<!-- The chart itself is auto refreshed on a different schedule in js code -->
<meta http-equiv="refresh" content="1200">
<head>
    <title></title>
</head>
<body>
<div id="chartDiv" style="cursor: none;"></div>
<p id="debug">Debug</p>
<button onclick="unhideCursor()">Unhide Cursor</button>
<p id="cursorMode">Cursor Hidden</p>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script>
  var REFRESH_TIME_SECS = 10

  // Helper function to get url parameters
  var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
      sParameterName = sURLVariables[i].split('=');

      if (sParameterName[0] === sParam) {
        return sParameterName[1] === undefined ? true : sParameterName[1];
      }
    }
  };

  var timedMeasurementSortFunction = function sort(tuple1, tuple2) {
    // The tuples are of the form [timestamp, measurement]
    // We only care about sorting the timestamps
    return tuple1[0] - tuple2[0];
  }

  google.load('visualization', '1', {'packages':['corechart']});

  // Set a callback to run when the Google Visualization API is loaded.
  google.setOnLoadCallback(drawChart);

  var dataRows = [];

  // Start the auto refresh
  autoRefresh();

  var refreshTimer = REFRESH_TIME_SECS;
  function autoRefresh() {
    if (refreshTimer > 0) {
      $("#debug").html("refreshing in:" + refreshTimer + "sec");
    } else {
      drawChart();
      // 10sec auto refresh
      refreshTimer = REFRESH_TIME_SECS;
    }
    refreshTimer -= 1;
    setTimeout(autoRefresh, 1000);
  }

  var chartOptions = {
    hAxis: {
      title: 'Time'
    },
    vAxis: {
      title: 'Watts'
    },
    colors: ['#2299EE'],
    width: 800,
    height: 420,
  };

  function drawChart() {
    var jsonUrl = "http://energymonitor-1090.appspot.com/readData";

    var historyValue = getUrlParameter('history');
    if (dataRows.length == 0) {
      jsonUrl += "?history=";
      if (historyValue != null) {
        $("#debug").html("historyValue: " + historyValue);
        jsonUrl += historyValue;
      } else {
        // Default lookback is 4 hours
        jsonUrl += "4";
        historyValue = 4;
      }
    } else {
      jsonUrl += "?starttime=";
      jsonUrl += dataRows[dataRows.length - 1][0].toGMTString();
    }

    $("#debug").html("Calling: " + jsonUrl);

    $.getJSON(jsonUrl).done(function (jsonData) {
      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'Time');
      data.addColumn('number', 'Watts');

      $.each(jsonData, function (key, item) {
        dataRows.push([new Date(Date.parse(item.timestamp)), item.value]);
      });

      // TODO: Not sure why we need to sort here, in theory the items that get pushed
      // onto the array should already be sorted, but thi seems to be a problem so keeping
      // this here for now.
      dataRows.sort(timedMeasurementSortFunction);
      // Trim off the old data as we go
      var cutoffIndex = 0;
      var cutoffTime = new Date(new Date() - (historyValue * 60 * 60 * 1000));
      while (cutoffIndex < dataRows.length && dataRows[cutoffIndex][0] < cutoffTime) {
        cutoffIndex += 1;
      }
      dataRows = dataRows.slice(cutoffIndex, dataRows.length);
      // Add the new rows
      data.addRows(dataRows);


      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.LineChart(document.getElementById('chartDiv'));
      chart.draw(data, chartOptions);
    });
  }

  // By default we hide the cursor over the chart area, but if we can call this function
  // to unhide it when using the chart on a desktop
  function unhideCursor() {
    $('#chartDiv').css("cursor", "auto");
    $('#cursorMode').html("Cursor normal");
  }
</script>
</body>
</html>
