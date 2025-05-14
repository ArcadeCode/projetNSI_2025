from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
from app.fonts import Font
from app import APP_VERSION

# TODO: Fix spaghettis layout thing.
class TitleScreenWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TitleScreenWidget, self).__init__(**kwargs)
        
        # Puisque nous sommes dans un Screen, nous pouvons utiliser 
        # un FloatLayout pour occuper tout l'espace disponible
        layout_principal = FloatLayout(size_hint=(1, 1))
        
        # Créer un BoxLayout pour organiser verticalement nos éléments
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 0.4),  # Taille du contenu par rapport à l'écran
            pos_hint={'center_x': 0.5, 'center_y': 0.5},  # Position centrée sur l'écran
            spacing=20  # Espacement entre les widgets
        )
        
        # Ajouter les widgets au content_layout
        content_layout.add_widget(
            Label(
                text="Sportify",
                font_size=24,
                font_name=Font.Montserrat_Bold,
                size_hint_y=None,
                height=50,
                halign='center'
            )
        )
        
        content_layout.add_widget(
            Label(
                text=f"version : {APP_VERSION}",
                font_size=12,
                font_name=Font.Montserrat_Bold,
                size_hint_y=None,
                height=30,
                halign='center'
            )
        )
        
        # Ajouter un spacer (espace vide) pour pousser le bouton vers le bas
        content_layout.add_widget(Widget(size_hint_y=0.2))
        
        # Créer et ajouter le bouton
        self.btn = Button(
            text="Sign in",
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5}  # Centre le bouton horizontalement dans le BoxLayout
        )
        self.btn.bind(on_press=self.on_sign_in_press)
        content_layout.add_widget(self.btn)
        
        # Ajouter le layout de contenu au layout principal
        layout_principal.add_widget(content_layout)
        
        # Ajouter le layout principal au widget
        self.add_widget(layout_principal)
        
        Logger.debug(f"{self} was initialized")
    
    def on_sign_in_press(self, instance):
        # Chercher le parent Screen puis appeler sa méthode switch_screen
        screen = self.get_parent_screen()
        if screen:
            screen.switch_screen('home')
            Logger.debug("Switching to home screen")
        else:
            Logger.error("Cannot find parent screen")
   
    def get_parent_screen(self):
        # Remonter la hiérarchie des widgets pour trouver le Screen parent
        parent = self.parent
        while parent:
            if hasattr(parent, 'switch_screen'):
                return parent
            parent = parent.parent
        return None