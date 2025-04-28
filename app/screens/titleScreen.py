from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from app.widgets import TitleScreenWidget

from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from app.widgets import TitleScreenWidget

class TitleScreen(Screen):
    '''Screen for the title menu'''

    def switch_screen(self, screen_name):
        if self.manager:  # Ensure the ScreenManager is properly attached
            Logger.debug(f"{self}: Switching from {self.name} to {screen_name}")
            self.manager.current = screen_name
        else:
            Logger.error("{self}: Screen manager not found")
    
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(TitleScreen, self).__init__(**kwargs)
        self.add_widget(TitleScreenWidget())
        Logger.debug(f"{self}: was initialized, children are : {self.children}")