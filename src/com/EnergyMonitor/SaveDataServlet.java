package com.EnergyMonitor;

import com.google.common.base.Strings;
import com.googlecode.objectify.ObjectifyService;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Created by cortana101 on 10/5/15.
 */
public class SaveDataServlet extends HttpServlet {

  @Override
  public void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    resp.setContentType("text");
    String measurement = req.getParameter("measurement");
    if (!Strings.isNullOrEmpty(measurement)) {
      try {
        float measurementValue = Float.parseFloat(measurement);
        // write the value into datastore
        Measurement measurementData = new Measurement(measurementValue);
        ObjectifyService.ofy().save().entity(measurementData).now();
        resp.getWriter().write("Successfully parsed " + measurement + " timestamp: ");
      } catch (NumberFormatException e) {
        resp.getWriter().write("Error, unable to parse value: " + measurement + " as float");
      }
    } else {
      resp.getWriter().write("Measurement value was not specified");
    }
  }
}
