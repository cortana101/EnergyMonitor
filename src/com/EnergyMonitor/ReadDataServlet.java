package com.EnergyMonitor;

import com.google.appengine.api.datastore.Query;

import com.google.gson.Gson;
import com.googlecode.objectify.ObjectifyService;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Calendar;
import java.util.List;
import java.util.Date;
import java.util.TimeZone;

/**
 * Created by cortana101 on 10/5/15.
 */
public class ReadDataServlet extends HttpServlet {
  @Override
  public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    resp.setContentType("application/json");
    Gson gson = new Gson();
    // Get a time which represents 24 hours before the current time as the starting point for our daily graph
    Date currentTime = new Date();
    Calendar cal = Calendar.getInstance();
    cal.setTime(currentTime);
    cal.add(Calendar.HOUR, -24);
    Date filterTime = cal.getTime();
    List<Measurement> measurements = ObjectifyService.ofy()
        .load()
        .type(Measurement.class)
        .order("-timestamp")
        .filter("timestamp >= ", filterTime)
        .list();
    // For every record that we get out, transform the timestamp so instead of UTC it is local to SF
    for (Measurement measurement : measurements) {
      Calendar timezoneCal = Calendar.getInstance();
      timezoneCal.setTime(measurement.timestamp);
      timezoneCal.add(Calendar.MILLISECOND, TimeZone.getTimeZone("America/Los_Angeles").getRawOffset());
      measurement.timestamp = timezoneCal.getTime();
    }
    String output = gson.toJson(measurements);
    resp.getWriter().write(output);
  }
}
