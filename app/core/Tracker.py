import threading
from time import sleep, time_ns
from datetime import datetime
from plyer import gps
from dataclasses import dataclass

@dataclass
class Point:
    '''A point is a representation of all data at a given datetime'''
    latitude: float
    longitude: float
    altitude: float
    precision: float
    timestamp: datetime
    speed: float = 0.0  # m/s
    acceleration: float = 0.0  # m/s²
    heart_rate: int = None  # BPM

class SensorGPS:
    def get_data(self):
        # Simulation de récupération des données GPS
        return {
            "latitude": 48.8566,
            "longitude": 2.3522,
            "altitude": 35.0,
            "precision": 3.0
        }

class SensorManager:
    '''Manage sensors and save data'''
    
    def __init__(self):
        self.sensors = [SensorGPS()]  # Liste des capteurs utilisés
        self.dataset = []  # Stocke les points


    def get_dataset_size(self):
        from pympler import asizeof
        total_size = asizeof.asizeof(self.dataset)

        # Conversion en unités lisibles
        units = ["bytes", "KB", "MB", "GB"]
        size = total_size
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        print(f"Total memory usage: {total_size} bytes ({size:.2f} {units[unit_index]}) pour {len(self.dataset)} points.")
        return total_size


    def dataset_add_point(self):
        '''Récupère les données et ajoute un point au dataset'''
        gps_data = self.sensors[0].get_data()  # Simule un GPS
        point = Point(
            latitude=gps_data["latitude"],
            longitude=gps_data["longitude"],
            altitude=gps_data["altitude"],
            precision=gps_data["precision"],
            timestamp=datetime.now()
        )
        self.dataset.append(point)
        print(f"[INFO] Point ajouté : {point}")

class Tracker:
    '''Track user movements'''
    def __init__(self):
        self.trackerEnabled = False
        self.sensorManager = SensorManager()
        self.thread = None

    def start(self, delta_time: int = 5):
        '''Lance le tracking dans un thread'''
        self.trackerEnabled = True
        self.thread = threading.Thread(target=self.tracking, args=(delta_time,))
        self.thread.start()

    def stop(self):
        '''Arrête le tracking'''
        self.trackerEnabled = False
        if self.thread:
            self.thread.join()

    def tracking(self, delta_time: int = 5):
        '''Boucle de tracking exécutée dans un thread séparé'''
        while self.trackerEnabled:
            self.sensorManager.dataset_add_point()
            sleep(delta_time)  # Attendre entre les acquisitions

    def save_tracking(self) :
        pass

# Exemple d'utilisation
tracker = Tracker()
tracker.start(delta_time=0.1)  # Récupération toutes les 0.1s

sleep(15)  # Laisser tourner quelques secondes
tracker.stop()
print(tracker.sensorManager.dataset)
tracker.sensorManager.get_dataset_size()