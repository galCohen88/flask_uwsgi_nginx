from drone.consts import SENSOR_MODE_PASSIVE_TRACKING
from drone.entities import Sensor


def listen():
    sensor1 = Sensor(1, 2)
    sensor2 = Sensor(3, 4)
    sensor3 = Sensor(6, 10)

    # detached..
    sensor1.scan_perimeter()
    sensor2.scan_perimeter()
    sensor3.scan_perimeter()

    while True:
        sensors = [sensor1, sensor2, sensor3]
        detection_sensors = [i for i, x in enumerate(sensors) if x.mode == SENSOR_MODE_PASSIVE_TRACKING]

