from machine import Pin, I2C
import utime
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from mfrc522 import MFRC522

 
# LCD setup
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
 
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
 
# RFID setup
#rdr = MFRC522(spi_id=0, sck=2, mosi=3, miso=4, rst=6, cs=5)
rdr = MFRC522(spi_id=1, sck=10, mosi=11, miso=12, rst=14, cs=13)
 
def read_rfid():
    (status, tag_type) = rdr.request(rdr.REQIDL)
    if status == rdr.OK:
        (stat, uid) = rdr.SelectTagSN()
        if stat == rdr.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            return str(card)
    return None

# Create a csv file to output the card reads:
outfile = open('card_reads.csv', 'w')
outfile.write("RFID NUMBER,YEAR,MONTH,DAY,HOUR,MINUTE,SECOND\n")
outfile.close()

# Create a function to write the card reads (and date/time of the reads) to the csv
# file each time a tag or card is swiped:
def store_data(card):
    with open('card_reads.csv', 'a') as outfile:
        outfile.write(card)
        outfile.write(",")
        now = utime.localtime()
        outfile.write(str(now[0]))
        outfile.write(",")
        outfile.write(str(now[1]))
        outfile.write(",")
        outfile.write(str(now[2]))
        outfile.write(",")
        outfile.write(str(now[3]))
        outfile.write(",")
        outfile.write(str(now[4]))
        outfile.write(",")
        outfile.write(str(now[5]))
        outfile.write("\n")
        return(card)
 
while True:
    lcd.clear()
    lcd.putstr("Scan RFID tag...")
    utime.sleep(.5)
   
    card = read_rfid()
    if card:
        lcd.clear()
        lcd.putstr(card)
        store_data(card)
        utime.sleep(2)
       
    else:
            lcd.clear()
            lcd.putstr("No tag detected")
            utime.sleep(.5)
           
utime.sleep_ms(500)