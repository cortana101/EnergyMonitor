<%@ page import="java.net.URL" %>
<%@ page import="java.net.HttpURLConnection" %>
<%@ page import="com.google.gson.JsonParser" %>
<%@ page import="com.google.gson.JsonElement" %>
<%@ page import="java.io.InputStreamReader" %>
<%@ page import="java.io.InputStream" %>
<%@ page import="com.google.gson.JsonObject" %>
<%@ page import="com.google.gson.JsonArray" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<script src="js/Chart.js"></script>
<script src="js/jquery-2.1.4.min.js"></script>
<html>
<head>
    <title></title>
</head>
<body>
<canvas id="chartSurface" width="600" height="400">
</canvas>
<p id="debug">Debug</p>
<%--<%--%>
  <%--URL url = new URL("http://1.energymonitor-1090.appspot.com/readData");--%>
  <%--HttpURLConnection req = (HttpURLConnection) url.openConnection();--%>
  <%--req.connect();--%>

  <%--JsonParser jp = new JsonParser();--%>
  <%--JsonElement root = jp.parse(new InputStreamReader((InputStream) req.getContent()));--%>
  <%--JsonArray measurements = root.getAsJsonArray();--%>
  <%--%>--%>
  <%--<table> <%--%>
  <%--for (JsonElement measurement : measurements) {--%>
    <%--String timestamp = measurement.getAsJsonObject().get("timestamp").getAsString();--%>
    <%--String value = measurement.getAsJsonObject().get("value").getAsString();--%>
    <%--pageContext.setAttribute("timestamp", timestamp);--%>
    <%--pageContext.setAttribute("value", value);--%>
    <%--%>--%>
    <%--<tr>--%>
      <%--<td>${fn:escapeXml(timestamp)}</td>--%>
      <%--<td>${fn:escapeXml(value)}</td>--%>
    <%--</tr>--%>
    <%--<%--%>
  <%--}--%>
<%--%>--%>
  </table>
</body>
</html>
<script>
  //TODO: The basics of the charts are working now, though the labels and the scales need to be tweaked.
  // Seems like the linear scaling that we want is only available in chart js 2.0 beta, we should upgrade
  // the js files to that version and play with the axis scaling

  var ctx = $("#chartSurface").get(0).getContext("2d");
  var chartValues = [];
  var chartTimestamps = [];
  $.getJSON("http://energymonitor-1090.appspot.com/readData").done(function(data) {
    $.each(data, function (key, item) {
      chartValues.push(item.value);
      chartTimestamps.push(item.timestamp)
    });
    $("#debug").html("Executed");
    $("#debug").html(chartValues[0].toString());
    var data = {
//      labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      labels: chartTimestamps,
      datasets: [
//        {
//          label: "My First dataset",
//          fillColor: "rgba(220,220,220,0.2)",
//          strokeColor: "rgba(220,220,220,1)",
//          pointColor: "rgba(220,220,220,1)",
//          pointStrokeColor: "#fff",
//          pointHighlightFill: "#fff",
//          pointHighlightStroke: "rgba(220,220,220,1)",
//          data: [65.1, 59.5, 80.4, 81.2, 56, 55, 40]
//        },
        {
          label: "Power over time",
          fillColor: "rgba(0,220,220,0.2)",
          strokeColor: "rgba(0,220,220,1)",
          pointColor: "rgba(0,220,220,1)",
          pointStrokeColor: "#0ff",
          pointHighlightFill: "#0ff",
          pointHighlightStroke: "rgba(0,220,220,1)",
          data: chartValues
        },
      ]
    };

    var newChart = new Chart(ctx).Line(data, {
      bezierCurve: false,
      pointDot: false,
    });
  });


</script>
