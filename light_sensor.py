import time
import board
import adafruit_tcs34725

class LightSensor:
    def __init__(self, gain=4, integration_time=150):
        self.i2c = board.I2C()
        self.sensor = adafruit_tcs34725.TCS34725(self.i2c)
        self.sensor.gain = gain
        self.sensor.integration_time = integration_time

    def read_lux(self):
        return self.sensor.lux
    
    def read_rgbc(self):
        return self.sensor.color_raw
    
    def read_color_temp(self):
        return self.sensor.color_temperature
