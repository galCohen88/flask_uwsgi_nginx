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

        for idx in detection_sensors:
            if is_a_threat(sensors[idx]):
                handle_threat(sensors[idx])


def handle_threat(sensor):
    sensor.land_drone()


def choose_sensor(all_sensors_detected_the_threat):
    pass


def is_a_threat(sensor):
    # return True if distance & speed & bearing is calculated to threat on compound

    drone_distance_from_sensor = sensor.calculate_distance_from_object(sensor.tracked_drone_movement[-1])
    velocity_vector = sensor.velocity_vector

    if 'bearing, speed and distance considered a threat':
        return True
    return False
