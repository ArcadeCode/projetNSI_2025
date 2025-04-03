from app.fonts import Font
from app import APP_VERSION

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class TitleScreenWidget(Screen):
    def switch_screen(self, screen_name):
        if self.manager:  # Ensure the ScreenManager is properly attached
            self.manager.current = screen_name
    
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
        self.add_widget(
            Button(
                text="Sign in",
                size_hint=(.5, .5),
                pos_hint={'center_x': .5, 'center_y': .5}
            )
        )