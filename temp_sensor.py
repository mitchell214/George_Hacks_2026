from grove.grove_temperature_sensor import GroveTemperatureSensor

class TSensor:
    def __init__(self, channel):
        self.__init_sensor__(channel)

    def __init_sensor__(self, channel):
        self.sensor = GroveTemperatureSensor(channel)

    def read_temp(self):
        return self.sensor.temperature

    def format_temp(self, temperature):
        return 'Temperature: {0:.2f} °C'.format(temperature)