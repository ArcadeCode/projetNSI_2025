from app.fonts import Font
from app import APP_VERSION

from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.clock import Clock


class TitleScreenWidget(Widget):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(TitleScreenWidget, self).__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = 0

        # Assembly widget :
        self.add_widget(
            Label(text="Sportify",
                  font_size=24,
                  font_name=Font.Montserrat_Bold,
                  halign='center',
            )
        )
        self.add_widget(
            Label(text=f"version : {APP_VERSION}",
                  font_size=12,
                  font_name=Font.Montserrat_Bold
            )
        )
        self.add_widget(
            Widget(
                size_hint=(None, None),
                size=(200, 100))
        )

        self.btn = Button(
                text="Sign in",
                size_hint=(.5, .25),
                pos_hint={'center_x': .5, 'center_y': .5}
            )
        self.btn.bind(on_press=self.on_sign_in_press)
        self.add_widget(self.btn)  # Ajout du bouton au widget
        
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