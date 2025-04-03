import random as rand

class Mock_SensorGPS:
    def get_data(self, precision: int = 3):
        return {
            "latitude": round(rand.uniform(-90.0, 90.0), precision),
            "longitude": round(rand.uniform(-180.0, 180.0), precision),
            "altitude": round(rand.uniform(0.0, 8848.0), precision),  # De 0 à la hauteur de l'Everest
            "precision": precision
        }

class Mock_SensorBPM:
    def __init__(self, initial_bpm: int = 75):
        self.current_bpm = initial_bpm

    def get_data(self):
        variation = rand.randint(-3, 5)  # Légère augmentation ou diminution
        self.current_bpm = max(50, min(200, self.current_bpm + variation))  # Garder BPM dans une plage logique
        return {"heart_bpm": self.current_bpm}

class Mock_SensorSpeed:
    def __init__(self, initial_speed: float = 5.0):  # Un coureur commence à environ 5 m/s
        self.current_speed = initial_speed

    def get_data(self):
        acceleration = rand.uniform(-1.0, 1.5)  # Accélération réaliste pour un coureur
        self.current_speed = max(0, min(12, self.current_speed + acceleration))  # Limite à une vitesse max de sprinter
        return {
            "speed": round(self.current_speed, 2),
            "acceleration": round(acceleration, 2)
        }