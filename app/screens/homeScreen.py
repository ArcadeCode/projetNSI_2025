from kivy.uix.screenmanager import Screen
from app.widgets import HomeScreenWidget

class HomeScreen(Screen):
    '''Screen for the main menu'''

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(HomeScreen, self).__init__(**kwargs)
        self.add_widget(HomeScreenWidget())