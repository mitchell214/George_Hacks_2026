from grove.grove_temperature_sensor import GroveTemperatureSensor

class TSensor:
    def __init__(self, channel):
        self.sensor = GroveTemperatureSensor(channel)
        self.temp_reads = []

    def get_last_read_temp(self):
        if (len(self.temp_reads) == 0):
            return None
        
        return self.temp_reads[len(self.temp_reads) - 1]

    def read_temp(self):
        self.temp_reads.append(self.sensor.temperature)
        return self.get_last_read_temp()

    def formatted_temp(self):
        return 'Temperature: {0:.2f} °C'.format(self.get_last_read_temp())