import time, os, lcdlib, urllib2

NOISE_READING = 20 #By default we assume the noise inherent in the system contributes to 30 units of arduino DAC reading
INTEGRAL_NOISE = 1.7
ARDUINO_VOLTAGE = 3.3
INPUT_VOLTAGE = 120
BURDEN_RESISTANCE = 110
CORRECTION_MULTIPLIER = 1.085

INTEGRAL_MULTIPLIER = (ARDUINO_VOLTAGE / 4095 / BURDEN_RESISTANCE) * 2000 * INPUT_VOLTAGE * CORRECTION_MULTIPLIER
NOLOAD_VOLTAGE_GAIN = 2.0
CURRENT_VOLTAGE_DROP_FACTOR = 0.00384

# The number of watts delta we need from the previous reading before we trigger a new upload event
POWER_UPLOAD_DIFFERENCE_THRESHOLD = 5.0

def read_pin_three():
    file = open('/proc/adc3', 'r')
    file.seek(0)
    value = file.read(16)
    file.close()
    value = value[5:]
    value_int = int(value)
    return value_int

def get_power(list_of_samples):
    running_total = 0
    for sample in list_of_samples:
        running_total += sample
    mean = float(running_total) / len(list_of_samples)
    integral = 0
    for sample in list_of_samples:
        integral += abs(sample - mean)
    integral /= float(len(list_of_samples))
    return integral - INTEGRAL_NOISE

def upload_data(power):
    try:
        response = urllib2.urlopen('http://1.energymonitor-1090.appspot.com/saveData?measurement=' + power).read()
        lcdlib .print_second_line(response[:16])
    except urllib2.HTTPError:
        lcdlib.print_second_line("HTTP Error")

# use a counter to determine sampling periods
counter = 0
samples = []
lcdlib.init_lcd()
previous_power = 0.0

while(True):
    samples += [read_pin_three()]
    time.sleep(0.001)
    counter += 1
    # When we've done 400ms, calculate the power draw in this entire segment and repeat
    if (counter >= 1000):
        power = get_power(samples)
        power *= INTEGRAL_MULTIPLIER * ((120 + NOLOAD_VOLTAGE_GAIN - (power * CURRENT_VOLTAGE_DROP_FACTOR)) / 120)
        if power < 0:
            power = 0.0
        if (abs(power - previous_power) > POWER_UPLOAD_DIFFERENCE_THRESHOLD):
            upload_data(str.format("{:.2f}", power))
            previous_power = power
        lcdlib.print_first_line(str.format("{:.2f}W", power))
        counter = 0
        samples = []

