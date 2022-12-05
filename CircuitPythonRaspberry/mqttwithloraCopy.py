import time
# Import RFM9x
import adafruit_rfm9x
# Configure LoRa Radio
# Import Blinka Libraries
import busio
import time
import paho.mqtt.client as mqtt
import digitalio
import board

def on_publish(client, userdata, mid):
    print("sent a message")


mqttClient = mqtt.Client("greenhouse_alarm")
mqttClient.on_publish = on_publish
mqttClient.username_pw_set(username="gateway_broker", password="123456789")
mqttClient.connect('localhost', 1883)
# start a new thread
mqttClient.loop_start()

CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0, crc=True)
prev_packet = None

print('Waiting for packets...')

while True:
    packet = None
    info = None
    # check for packet rx
    packet = rfm9x.receive(timeout = 5.0, with_header = True)
    if packet is None:
        continue
        # Wait to receive packets.
#         print("Waiting for packets...")
    elif packet is not None:
        print('Received (raw bytes): {0}'.format(packet))
        info = mqttClient.publish(
            topic='greenhouse/alarm',
            payload=packet,
            qos=1)
   