from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from datetime import datetime
import math

class RunHistoryCard(BoxLayout):
    """Widget représentant une course individuelle dans l'historique"""
    
    def __init__(self, run_data, **kwargs):
        super(RunHistoryCard, self).__init__(**kwargs)
        self.run_data = run_data
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(150)
        self.padding = [10, 10]
        self.spacing = 5
        
        # Couleurs différentes pour les vraies courses et les simulations
        with self.canvas.before:
            if run_data.get('is_mock', False):
                Color(0.8, 0.8, 1, 1)  # Bleu clair pour les simulations
            else:
                Color(0.7, 1, 0.7, 1)  # Vert clair pour les vraies courses
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Titre avec indicateur de simulation si nécessaire
        title_text = run_data['name']
        if run_data.get('is_mock', False):
            title_text += " [SIMULATION]"
            
        title = Label(
            text=title_text,
            size_hint_y=None,
            height=dp(30),
            bold=True,
            color=(0, 0, 0, 1)
        )
        self.add_widget(title)
        
        # Date et heure
        try:
            date_obj = datetime.strptime(run_data['start_time'], "%Y-%m-%d %H:%M:%S")
            date_str = date_obj.strftime("%d/%m/%Y à %H:%M")
        except:
            date_str = run_data['start_time']
            
        date_label = Label(
            text=date_str,
            size_hint_y=None,
            height=dp(20),
            color=(0.3, 0.3, 0.3, 1)
        )
        self.add_widget(date_label)
        
        # Informations de la course
        info_layout = GridLayout(cols=2, size_hint_y=None, height=dp(60))
        
        # Distance
        distance = run_data.get('distance_meters', 0)
        distance_str = f"{distance:.1f} m"
        if distance >= 1000:
            distance_str = f"{distance/1000:.2f} km"
            
        info_layout.add_widget(Label(text="Distance:", halign='right', color=(0, 0, 0, 1)))
        info_layout.add_widget(Label(text=distance_str, halign='left', color=(0, 0, 0, 1)))
        
        # Durée
        seconds = run_data.get('duration_seconds', 0)
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        info_layout.add_widget(Label(text="Durée:", halign='right', color=(0, 0, 0, 1)))
        info_layout.add_widget(Label(text=duration_str, halign='left', color=(0, 0, 0, 1)))
        
        # Vitesse moyenne
        if seconds > 0:
            speed = (distance / seconds) * 3.6  # en km/h
            speed_str = f"{speed:.1f} km/h"
        else:
            speed_str = "N/A"
            
        info_layout.add_widget(Label(text="Vitesse moyenne:", halign='right', color=(0, 0, 0, 1)))
        info_layout.add_widget(Label(text=speed_str, halign='left', color=(0, 0, 0, 1)))
        
        self.add_widget(info_layout)
        
        # Bouton pour voir les détails
        details_button = Button(
            text="Voir détails",
            size_hint_y=None,
            height=dp(30),
            background_color=(0.3, 0.6, 0.9, 1)
        )
        details_button.bind(on_press=self.show_details)
        self.add_widget(details_button)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def show_details(self, instance):
        # Créer un popup avec les détails supplémentaires
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Titre
        title_text = self.run_data['name']
        if self.run_data.get('is_mock', False):
            title_text += " [SIMULATION]"
        content.add_widget(Label(text=title_text, size_hint_y=None, height=dp(30), font_size='18sp'))
        
        # Nombre de points enregistrés
        points_count = len(self.run_data.get('coordinates', []))
        content.add_widget(Label(
            text=f"Points GPS enregistrés: {points_count}",
            size_hint_y=None, 
            height=dp(30)
        ))
        
        # Listing des coordonnées (limité aux 5 premiers points)
        if points_count > 0:
            coords_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(30*min(5, points_count)))
            coords_layout.add_widget(Label(
                text="Échantillon de coordonnées:",
                size_hint_y=None,
                height=dp(30),
                halign='left'
            ))
            
            for i, coord in enumerate(self.run_data.get('coordinates', [])[:5]):
                coords_layout.add_widget(Label(
                    text=f"Point {i+1}: Lat {coord.get('latitude', 0):.6f}, Lon {coord.get('longitude', 0):.6f}",
                    size_hint_y=None,
                    height=dp(20),
                    font_size='12sp'
                ))
            
            content.add_widget(coords_layout)
        
        # Bouton de fermeture
        close_button = Button(text="Fermer", size_hint_y=None, height=dp(40))
        content.add_widget(close_button)
        
        popup = Popup(
            title="Détails de la course",
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class RunHistoryScreen(Screen):
    """Écran affichant l'historique des courses"""
    
    def __init__(self, history_manager, **kwargs):
        super(RunHistoryScreen, self).__init__(**kwargs)
        self.history_manager = history_manager
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # En-tête
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(Label(text="Historique des courses", size_hint_x=0.7, font_size='20sp'))
        
        back_button = Button(text="Retour", size_hint_x=0.3)
        back_button.bind(on_press=self.go_back)
        header.add_widget(back_button)
        
        layout.add_widget(header)
        
        # Contenu scrollable pour les courses
        scroll_view = ScrollView()
        self.history_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.history_container.bind(minimum_height=self.history_container.setter('height'))
        
        scroll_view.add_widget(self.history_container)
        layout.add_widget(scroll_view)
        
        self.add_widget(layout)
        
        # Charger les données dès l'initialisation
        self.load_history()
    
    def load_history(self):
        # Vider le contenu actuel
        self.history_container.clear_widgets()
        
        # Récupérer l'historique
        runs = self.history_manager.get_all_runs()
        
        if runs:
            for run in runs:
                # Créer une carte pour chaque course
                run_card = RunHistoryCard(run)
                self.history_container.add_widget(run_card)
        else:
            # Message si aucune course n'est enregistrée
            self.history_container.add_widget(Label(
                text="Aucune course enregistrée",
                size_hint_y=None,
                height=dp(50)
            ))
    
    def go_back(self, instance):
        # Retourner à l'écran précédent
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'home'