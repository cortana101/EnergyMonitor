package com.EnergyMonitor;

import com.google.common.base.Strings;
import com.google.common.collect.Lists;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.googlecode.objectify.ObjectifyService;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Created by cortana101 on 10/5/15.
 */
public class ReadDataServlet extends HttpServlet {
  private static final String DATE_FORMAT_PATTERN = "EEE, dd MMM yyyy HH:mm:ss z";

  @Override
  public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    resp.setContentType("application/json");
    String history = req.getParameter("history");
    String startTime = req.getParameter("starttime");
    // Default history goes back 12 hours
    int historyHours = -12;
    if (!Strings.isNullOrEmpty(history)) {
      try {
        historyHours = Integer.parseInt(history);
        historyHours = -historyHours;
      } catch (NumberFormatException e) {
        resp.getWriter().write("Error, unable to parse value: " + history + " as int");
        return;
      }
    }
    Date currentTime = new Date();
    Calendar cal = Calendar.getInstance();
    cal.setTime(currentTime);
    cal.add(Calendar.HOUR, historyHours);
    Date filterTime = cal.getTime();

    if (!Strings.isNullOrEmpty(startTime)) {
      try {
        DateFormat df = new SimpleDateFormat(DATE_FORMAT_PATTERN, Locale.ENGLISH);
        filterTime = df.parse(startTime);
      } catch (ParseException e) {
        resp.getWriter().write("Error, unable to parse date: " + startTime);
        resp.getWriter().write("Error message:" + e.getMessage());
        resp.getWriter().write("Stack:" + e.getStackTrace());
      }
    }

    Gson gson = new GsonBuilder().setDateFormat(DATE_FORMAT_PATTERN).create();
    List<Measurement> measurements = ObjectifyService.ofy()
        .load()
        .type(Measurement.class)
        .order("-timestamp")
        .filter("timestamp > ", filterTime)
        .list();
    measurements = Lists.reverse(measurements);
    String output = gson.toJson(measurements);
    resp.getWriter().write(output);
  }
}
