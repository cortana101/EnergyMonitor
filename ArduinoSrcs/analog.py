import time, os, lcdlib

NOISE_READING = 20 #By default we assume the noise inherent in the system contributes to 30 units of arduino DAC reading
INTEGRAL_NOISE = 1.7
ARDUINO_VOLTAGE = 3.3
INPUT_VOLTAGE = 120
BURDEN_RESISTANCE = 110
CORRECTION_MULTIPLIER = 1.085

INTEGRAL_MULTIPLIER = (ARDUINO_VOLTAGE / 4095 / BURDEN_RESISTANCE) * 2000 * INPUT_VOLTAGE * CORRECTION_MULTIPLIER
NOLOAD_VOLTAGE_GAIN = 2.0
CURRENT_VOLTAGE_DROP_FACTOR = 0.00384

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

# use a counter to determine sampling periods
counter = 0
samples = []
lcdlib.init_lcd()

while(True):
	# lcdlib.print_first_line(" " * 16)
	# lcdlib.print_first_line(str(read_pin_three()))
	samples += [read_pin_three()]
	time.sleep(0.001)
	counter += 1
	# When we've done 400ms, calculate the power draw in this entire segment and repeat
	if (counter >= 1000):
		power = get_power(samples)
		power *= INTEGRAL_MULTIPLIER * ((120 + NOLOAD_VOLTAGE_GAIN - (power * CURRENT_VOLTAGE_DROP_FACTOR)) / 120)
		print str.format("power: {:.2f}", power)
		if power < 0:
			power = 0.0
		lcdlib.print_first_line(str.format("{:.2f}W", power))
		counter = 0
		samples = []

