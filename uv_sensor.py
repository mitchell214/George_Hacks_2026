from grove.grove_i2c_uv_sensor_veml6070 import GroveI2CUVLightSensor

class UVSensor:
    def __init__(self):
        self.sensor = GroveI2CUVLightSensor()

    def read_uv_intensity(self):
        return self.sensor.get_uv_intensity()