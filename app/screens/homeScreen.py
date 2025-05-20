from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivy.logger import Logger

from app.screens.historicScreen import RunHistoryScreen

import datetime
import json
import os
import platform

# TODO: Ré-organiser un peu ce fichier

# Vérification de la disponibilité du GPS
GPS_AVAILABLE = True
try:
    from plyer import gps
    # Test simple pour vérifier si l'implémentation est disponible
    gps.start(minTime=1000, minDistance=1)
    gps.stop()
except (ImportError, NotImplementedError):
    GPS_AVAILABLE = False
    Logger.warning("Tracker: GPS not available on this system")

class GPSTracker:
    def __init__(self):
        self.running = False
        self.coordinates = []
        self.start_time = None
        self.end_time = None
        self.mock_mode = not GPS_AVAILABLE
        
    def start_tracking(self):
        self.running = True
        self.coordinates = []
        self.start_time = datetime.datetime.now()
        
        # En mode simulation, ajoutons un mock du tracker gps
        if self.mock_mode:
            # Planifie l'ajout de points GPS simulés
            Clock.schedule_interval(self.add_mock_point, 2)
        
    def stop_tracking(self):
        self.running = False
        self.end_time = datetime.datetime.now()
        
        # Arrêt de la simulation si nécessaire
        if self.mock_mode:
            Clock.unschedule(self.add_mock_point)
        
    def add_point(self, lat, lon):
        if self.running:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.coordinates.append({
                'latitude': lat,
                'longitude': lon,
                'timestamp': timestamp
            })
    
    def add_mock_point(self, dt):
        """Ajoute un point GPS simulé"""
        if not self.running:
            return False
            
        import random
        # Crée un parcours simulé qui ressemble à un déplacement réel
        # Si nous n'avons pas encore de coordonnées, commençons quelque part
        if not self.coordinates:
            base_lat, base_lon = 48.8566, 2.3522  # Paris, par exemple
        else:
            # Sinon continuons depuis le dernier point
            base_lat = self.coordinates[-1]['latitude']
            base_lon = self.coordinates[-1]['longitude']
            
        # Léger déplacement aléatoire (simulation d'un mouvement)
        lat = base_lat + random.uniform(-0.0001, 0.0001)
        lon = base_lon + random.uniform(-0.0001, 0.0001)
        
        self.add_point(lat, lon)
        return True
            
    def get_distance(self):
        """Une implémentation simple de la distance totale parcourue"""
        total_distance = 0
        for i in range(1, len(self.coordinates)):
            # Distance euclidienne simplifiée (à améliorer pour une vraie application)
            lat1, lon1 = self.coordinates[i-1]['latitude'], self.coordinates[i-1]['longitude']
            lat2, lon2 = self.coordinates[i]['latitude'], self.coordinates[i]['longitude']
            
            # Multiplication par un facteur pour convertir approximativement en mètres
            distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111000
            total_distance += distance
            
        return total_distance
    
    def get_duration(self):
        if not self.start_time:
            return 0
            
        end = self.end_time if self.end_time else datetime.datetime.now()
        return (end - self.start_time).total_seconds()
    
    def save_run(self, name=None):
        if not self.coordinates:
            return False
            
        if not name:
            name = f"Course_{self.start_time.strftime('%Y%m%d_%H%M%S')}"
            
        run_data = {
            'name': name,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            'duration_seconds': self.get_duration(),
            'distance_meters': self.get_distance(),
            'coordinates': self.coordinates,
            'is_mock': self.mock_mode
        }
        
        if not os.path.exists('runs') : os.makedirs('runs')
            
        # Sauvegarde les données localement dans un fichier JSON
        # Moins lourd que une DB en local
        file_path = f"runs/{name}.json"
        with open(file_path, 'w') as f:
            json.dump(run_data, f, indent=2)

        # TODO: Implémenter la sauvegarde network via une DB sur internet
            
        return file_path

class RunHistoryManager:
    def __init__(self):
        pass
        
    def get_all_runs(self):
        runs = []
        if not os.path.exists('runs'):
            return runs
            
        for filename in os.listdir('runs'):
            if filename.endswith('.json'):
                with open(f'runs/{filename}', 'r') as f:
                    run_data = json.load(f)
                    runs.append(run_data)
                    
        # Trie les courses par date (la plus récente d'abord)
        runs.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        return runs
    
    def get_run_details(self, run_name):
        file_path = f"runs/{run_name}.json"
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            return json.load(f)

class RunTrackerWidget(BoxLayout):
    gps_status = StringProperty('GPS déconnecté')
    run_status = StringProperty('Prêt')
    distance = StringProperty('0.0 m')
    duration = StringProperty('00:00:00')
    
    def __init__(self, **kwargs):
        super(RunTrackerWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.tracker = GPSTracker()
        self.history_manager = RunHistoryManager()
        
        # Configuration GPS si disponible
        if GPS_AVAILABLE:
            gps.configure(on_location=self.on_gps_location,
                         on_status=self.on_gps_status)
            self.gps_status = 'GPS disponible'
        else:
            self.gps_status = 'GPS non disponible - Mode simulation activé'
        
        # Interface utilisateur
        self.status_label = Label(text='État: Prêt')
        self.add_widget(self.status_label)
        
        self.gps_label = Label(text=f'GPS: {self.gps_status}')
        self.add_widget(self.gps_label)
        
        self.distance_label = Label(text='Distance: 0.0 m')
        self.add_widget(self.distance_label)
        
        self.time_label = Label(text='Durée: 00:00:00')
        self.add_widget(self.time_label)
        
        self.start_button = Button(text='Démarrer', on_press=self.toggle_tracking)
        self.add_widget(self.start_button)
        
        self.history_button = Button(text='Historique', on_press=self.show_history)
        self.add_widget(self.history_button)
        
        # Mise à jour régulière de l'interface
        Clock.schedule_interval(self.update_ui, 1)
    
    def toggle_tracking(self, instance):
        if not self.tracker.running:
            # Démarrer le suivi
            self.start_tracking()
            instance.text = 'Arrêter'
        else:
            # Arrêter le suivi
            self.stop_tracking()
            instance.text = 'Démarrer'
    
    def start_tracking(self):
        # Activer le GPS réel uniquement s'il est disponible
        if GPS_AVAILABLE:
            gps.start(minTime=1000, minDistance=1)
        
        self.tracker.start_tracking()
        self.run_status = 'En cours'
        
        if not GPS_AVAILABLE:
            self.gps_status = 'Mode simulation activé'
    
    def stop_tracking(self):
        # Désactiver le GPS réel uniquement s'il est disponible
        if GPS_AVAILABLE:
            gps.stop()
        
        self.tracker.stop_tracking()
        
        # Sauvegarder la course
        saved_path = self.tracker.save_run()
        if saved_path:
            self.run_status = f'Sauvegardé: {os.path.basename(saved_path)}'
        else:
            self.run_status = 'Arrêté (non sauvegardé)'
    
    def on_gps_location(self, **kwargs):
        # Appelé quand une nouvelle localisation GPS est disponible
        lat = kwargs.get('lat', 0)
        lon = kwargs.get('lon', 0)
        
        # Ajouter le point GPS
        self.tracker.add_point(lat, lon)
        
        # Mettre à jour le statut GPS
        self.gps_status = f'GPS: {lat:.6f}, {lon:.6f}'
    
    def on_gps_status(self, *args, **kwargs):
        # Si appelé par plyer.gps
        if kwargs and 'status' in kwargs:
            status = kwargs.get('status', '')
            self.gps_status = f'GPS: {status}'
        # Si appelé par le changement de propriété, ne rien faire
        # pour éviter une boucle infinie
    
    def update_ui(self, dt):
        # Mise à jour de l'ui
        self.status_label.text = f'État: {self.run_status}'
        self.gps_label.text = self.gps_status
        
        if self.tracker.running:
            # Mettre à jour la distance et la durée
            distance = self.tracker.get_distance()
            self.distance = f'{distance:.1f} m'
            self.distance_label.text = f'Distance: {self.distance}'
            
            duration_seconds = self.tracker.get_duration()
            hours, remainder = divmod(int(duration_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            self.time_label.text = f'Durée: {self.duration}'

    # Modification de la méthode show_history dans RunTrackerWidget
    def show_history(self, instance):
        """Affiche l'écran d'historique des courses"""

        # Version CLI
        runs = self.history_manager.get_all_runs()
        if runs:
            print("=== Historique des courses ===")
            for run in runs:
                mock_indicator = " [SIMULATION]" if run.get('is_mock', False) else ""
                print(f"{run['name']}{mock_indicator} - {run['distance_meters']:.1f}m - {run['duration_seconds']}s")
        else:
            print("Aucune course enregistrée")

        # Vérifier si l'écran d'historique existe déjà
        if not self.parent.parent.parent.has_screen('history'):
            # Créer l'écran d'historique
            history_screen = RunHistoryScreen(self.history_manager, name='history')
            self.parent.parent.parent.add_widget(history_screen)
        else:
            # Recharger l'historique si l'écran existe déjà
            history_screen = self.parent.parent.parent.get_screen('history')
            history_screen.load_history()
        
        # Passer à l'écran d'historique
        self.parent.parent.parent.transition.direction = 'left'
        self.parent.parent.parent.current = 'history'

# Main HomeScreenWidget
class HomeScreenWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(HomeScreenWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Ajout du widget de tracking GPS
        self.run_tracker = RunTrackerWidget()
        self.add_widget(self.run_tracker)
        
        # Vous pouvez ajouter d'autres widgets pour votre HomeScreen ici
        # ...

# Enfin le HomeScreen
class HomeScreen(Screen):
    '''Screen for the main menu'''
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(HomeScreen, self).__init__(**kwargs)
        self.add_widget(HomeScreenWidget())
