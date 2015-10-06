package com.EnergyMonitor;

import com.googlecode.objectify.ObjectifyService;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

/**
 * Created by cortana101 on 10/5/15.
 */
public class ObjectifyHelper implements ServletContextListener {
  public void contextInitialized(ServletContextEvent event) {
    ObjectifyService.register(Measurement.class);
  }

  public void contextDestroyed(ServletContextEvent event) {

  }
}
