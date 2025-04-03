from app.fonts import Font

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class HomeScreenWidget(Screen):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(HomeScreenWidget, self).__init__(**kwargs)

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