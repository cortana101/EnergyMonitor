package com.EnergyMonitor;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;
import com.googlecode.objectify.annotation.Index;

import java.util.Date;

/**
 * Created by cortana101 on 10/5/15.
 */
@Entity
public class Measurement {
  @Id public Long id;
  @Index
  public Date timestamp;
  public float value;

  public Measurement() {
    timestamp = new Date();
  }

  public Measurement(float value) {
    this();
    this.value = value;
  }
}
