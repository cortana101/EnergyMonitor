<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<script src="js/jquery-2.1.4.min.js"></script>
<html>
<head>
    <title></title>
</head>
<body>
<div id="chartDiv"></div>
<p id="debug">Debug</p>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script>
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

  google.load('visualization', '1', {'packages':['corechart']});

  // Set a callback to run when the Google Visualization API is loaded.
  google.setOnLoadCallback(drawChart);

  // Start the auto refresh
  autoRefresh();

  var refreshTimer = 30;
  function autoRefresh() {
    if (refreshTimer > 0) {
      $("#debug").html("refreshing in:" + refreshTimer + "sec");
    } else {
      drawChart();
      // 30sec auto refresh
      refreshTimer = 30;
    }
    refreshTimer -= 1;
    setTimeout(autoRefresh, 1000);
  }

  function drawChart() {

    var jsonUrl = "http://energymonitor-1090.appspot.com/readData";

    var historyValue = getUrlParameter('history');
    if (historyValue != null) {
      $("#debug").html("historyValue: " + historyValue);
      jsonUrl += "?history=" + historyValue;
    }

    $("#debug").html("Calling: " + jsonUrl);

    $.getJSON(jsonUrl).done(function (jsonData) {
      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'Time');
      data.addColumn('number', 'Watts');

      var dataRows = [];

      $.each(jsonData, function (key, item) {
        dataRows.push([new Date(item.timestamp), item.value]);
      });

      data.addRows(dataRows);

      var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Watts'
        },
        colors: ['#2299EE'],
        width: 800,
        height: 400,
      };

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.LineChart(document.getElementById('chartDiv'));
      chart.draw(data, options);
    });
  }
</script>
</body>
</html>
