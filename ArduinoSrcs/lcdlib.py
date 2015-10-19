import time, os, urllib2, json

STOCK_SYMBOLS = ["MSFT", "GOOG", "AAPL", "TSLA", "SPY"]

GPIO_MODE_PATH = os.path.normpath('/sys/devices/virtual/misc/gpio/mode/')
GPIO_PIN_PATH = os.path.normpath('/sys/devices/virtual/misc/gpio/pin/')

GPIO_FILENAME = "gpio"

pinMode = []
pinData = []

HIGH = 1
LOW = 0
INPUT = "0"
OUTPUT = "1"
INPUT_PU = "8"

# Gather together the list of GPIOs that we care about
for i in range(0, 18):
	pinMode.append(os.path.join(GPIO_MODE_PATH, 'gpio' + str(i)))
	pinData.append(os.path.join(GPIO_PIN_PATH, 'gpio' + str(i)))

# Set all pins to output mode and all output pins to low to start
for i in range(0, 18):
	file = open(pinMode[i], 'r+')
	file.write(OUTPUT)
	file.close()
	file = open(pinData[i], 'r+')
	file.write("0")
	file.close()

# Map indicies to well known constants
DB4 = 4 #D0
DB5 = 5 #D1
DB6 = 6 #D2
DB7 = 7 #D3
RS = 8
EN = 9
Backlight = 10

# Flag definitions
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00
LCD_FUNCTIONSET = 0x20

# Display control consts
LCD_DISPLAYCONTROL = 0x08
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLNKOFF = 0x00
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02

# Text direction consts
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTDECREMENT = 0x00
LCD_ENTRYMODESET = 0x04

# global variable holding the state of the display control commands
_displayControl = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLNKOFF

def read_state(pin):
	temp = ['']
	file = open(pinData[pin], 'r')
	temp[0] = file.read() 
	file.close()
	if ('0' in temp[0]):
		return "LOW"
	else:
		return "HIGH"

def print_state():
	print 'State: '
	for i in range(0, 18):
		print i 
		print read_state(i)

def write(pinIndex, val):
	file = open(pinData[pinIndex], 'r+')
	if (val):
		file.write("1")
	else:
		file.write("0")
	file.close()

def pulseEnable():
	write(EN, LOW)
	time.sleep(0.000001)
	write(EN, HIGH)
	time.sleep(0.000001)
	write(EN, LOW)
	time.sleep(0.001)

# Writes the 4 data pins for a given 4 bit uint
def write_4bits(data):
	for i in range(DB4, DB7 + 1):
		write(i, data & 0x01)
		data >>= 1
	pulseEnable()

def write_8bits(data):
	write_4bits(data >> 4)
	write_4bits(data)

def command(data):
	write(RS, LOW)
	write_8bits(data)

def write_data(data):
	write(RS, HIGH)
	write_8bits(data)

def display_on():
	global _displayControl
	_displayControl |= LCD_DISPLAYON 
	command(_displayControl | LCD_DISPLAYCONTROL)

def display_off():
	global _displayControl
	_displayControl &= ~LCD_DISPLAYON 
	command(_displayControl | LCD_DISPLAYCONTROL)

def clear_display():
	command(LCD_CLEARDISPLAY)
	time.sleep(0.002)

def set_entry_mode():
	command(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT)

def home():
	command(LCD_RETURNHOME)
	time.sleep(0.002)

def blink():
	global _displayControl
	_displayControl |= LCD_BLINKON
	command(LCD_DISPLAYCONTROL | _displayControl)

def blink_off():
	global _displayControl
	_displayControl &= ~LCD_BLINKON
	command(LCD_DISPLAYCONTROL | _displayControl)

def init_lcd():
	_displayFunction = LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS
	time.sleep(0.15)
	# init the RS and EN pins
	write(RS, LOW)
	write(EN, LOW)
	# turn on the backlight
	write(Backlight, HIGH)
	# set to 4 bit mode, pulse 3 times according to the manual
	for i in range(0, 3):
		write_4bits(0x03)
		time.sleep(0.005)
	# set to 8 bit interface
	write_4bits(0x02)
	# From here on we only use command and write_data to talk to the display because it has been init in 8 bit interface
	# Set lines and font size
	command(LCD_FUNCTIONSET | _displayFunction)
	# After this point, we have initialize the display and can no longer change the functionset
	display_off()
	clear_display()
	set_entry_mode()
	home()
	# sets display RAM locations to 0,0
	command(0x40)
	command(0x80)

	display_on()

def set_display_to_first_line():
	command(0x40)
	command(0x80)

def set_display_to_second_line():
	command(0x40)
	command(0xC0)

def write_hello_world():
	write_data(ord('H'))
	write_data(ord('e'))
	write_data(ord('l'))
	write_data(ord('l'))
	write_data(ord('o'))
	write_data(ord(' '))
	write_data(ord('W'))
	write_data(ord('o'))
	write_data(ord('r'))
	write_data(ord('l'))
	write_data(ord('d'))
	write_data(ord('!'))
	write_data(ord('!'))

def print_line(text):
	counter = 0
	for char in text:
		if (counter > 39):
			print "More than 1 line is printed, leaving " + text[40:]
			break;
		write_data(ord(char))
		counter += 1
	while (counter <= 39):
		# pad spaces at the end
		write_data(ord(' '))
		counter += 1

def print_first_line(text):
	set_display_to_first_line()
	print_line(text)

def print_second_line(text):
	set_display_to_second_line()
	print_line(text)

def get_stock_price(symbol):
	response = urllib2.urlopen('https://finance.google.com/finance/info?client=ig&q=NYSE:' + symbol).read()
	response = response[4:]
	data = json.loads(response)
	return (data[0]["l"], data[0]["c"], data[0]["cp"])

def get_first_line(symbol, price):
	spaces_count = 16 - len(symbol) - len(price)
	spaces = " " * spaces_count
	return symbol + spaces + price

def get_second_line(change, change_percent):
	spaces_count = 16 - len(change) - len(change_percent)
	spaces = " " * spaces_count
	return change + spaces + change_percent

def tick_stock_price():
	index = 0
	while(True):
		data = get_stock_price(STOCK_SYMBOLS[index])
		price = str(data[0])
		change = str(data[1])
		change_percent = str(data[2])
		print_first_line(get_first_line(STOCK_SYMBOLS[index], price))
		print_second_line(get_second_line(change, change_percent))
		# sleep 2 seconds between ticks
		time.sleep(2)
		index += 1
		if (index > (len(STOCK_SYMBOLS) - 1)):
			break
			index = 0

# the 2 things this lib should do
init_lcd()
#tick_stock_price()
