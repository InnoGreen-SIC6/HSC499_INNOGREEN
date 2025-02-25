import network
import urequests
import utime
import random
import dht
import machine

SSID = "17"
PASSWORD = "helloguys"

UBIDOTS_TOKEN = "BBUS-evGL3VfXHJqbTwDn5wiAKWKFJXxuJ7"
DEVICE_LABEL = "esp32_innogreen"
VARIABLE_TEMP = "temperature"
VARIABLE_HUM = "humidity"
VARIABLE_SOIL = "soil_moisture"
UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/esp32_innogreen/"

HEADERS = {
    "X-Auth-Token": UBIDOTS_TOKEN,
    "Content-Type": "application/json"
}

DHT_PIN = 4
SOIL_SENSOR_PIN = 34

dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))
soil_sensor = machine.ADC(machine.Pin(SOIL_SENSOR_PIN))
soil_sensor.atten(machine.ADC.ATTN_11DB) 

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Menghubungkan ke WiFi...")
    while not wlan.isconnected():
        utime.sleep(1)
    print(f"Terhubung ke WiFi! IP Address: {wlan.ifconfig()[0]}")

def send_data(temp, hum, soil):
    data = {
        VARIABLE_TEMP: {"value": temp},
        VARIABLE_HUM: {"value": hum},
        VARIABLE_SOIL: {"value": soil}
    }
    response = urequests.post(UBIDOTS_URL, json=data, headers=HEADERS)
    print(f"Response: {response.json()}")
    response.close()

connect_wifi()
while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        soil = soil_sensor.read() / 4095 * 100
        
        print(f"Temp: {temp}°C, Hum: {hum}%, Soil Moisture: {soil:.2f}%")
        send_data(temp, hum, soil)
        
    except Exception as e:
        print(f"Error: {e}")
    
    utime.sleep(10)  
