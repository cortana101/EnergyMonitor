package com.EnergyMonitor;

import com.google.gson.Gson;
import com.googlecode.objectify.ObjectifyService;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

/**
 * Created by cortana101 on 10/5/15.
 */
public class ReadDataServlet extends HttpServlet {
  @Override
  public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    resp.setContentType("application/json");
    Gson gson = new Gson();
    List<Measurement> measurements = ObjectifyService.ofy()
        .load()
        .type(Measurement.class)
        .order("-timestamp")
        .limit(10)
        .list();
    String output = gson.toJson(measurements);
    resp.getWriter().write(output);
  }
}
