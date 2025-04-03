import pytest
from time import sleep
from time import sleep
from app.tests.mocks.SensorMocks import Mock_SensorBPM, Mock_SensorGPS, Mock_SensorSpeed
from app.core.Tracker import Tracker

def test_run_expected_tracking_points():
    DELTA_TIME = 0.1
    TRACK_TIME = 1
    EXPECTED_POINTS = int(TRACK_TIME / DELTA_TIME)

    tracker = Tracker()
    tracker.sensorManager.sensors = [
        Mock_SensorGPS(),
        Mock_SensorBPM(),
        Mock_SensorSpeed(initial_speed=0),
    ]

    tracker.start(delta_time=DELTA_TIME)
    sleep(TRACK_TIME)
    tracker.stop()
    
    dataset_size = len(tracker.sensorManager.dataset)

    assert dataset_size == EXPECTED_POINTS, (
        f"Expected {EXPECTED_POINTS} points, got {dataset_size}"
    )


def test_dataset_memory_usage_on_one_thousand_points():
    MEMORY_LIMIT = 1_073_741_824 # = 1 Go
    DELTA_TIME = 0.0001
    TRACK_TIME = 1

    tracker = Tracker()
    tracker.sensorManager.sensors = [
        Mock_SensorGPS(),
        Mock_SensorBPM(),
        Mock_SensorSpeed(initial_speed=0),
    ]

    tracker.start(delta_time=DELTA_TIME)  # Simule un tracking
    sleep(TRACK_TIME)
    tracker.stop()

    dataset_size = tracker.sensorManager.get_dataset_size()

    assert dataset_size < MEMORY_LIMIT, (
        f"Dataset size too large: {dataset_size} bytes (limit: {MEMORY_LIMIT} bytes)"
    )