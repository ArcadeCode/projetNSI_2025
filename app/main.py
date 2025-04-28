from kivy.logger import Logger
import logging
# Dictionnaire de blacklistage avec les niveaux de log comme clés
LOG_BLACKLIST = {
    "DEBUG": ["Atlas", "GL", "ImageSDL2"],  # Pour le niveau DEBUG, on exclut les messages contenant 'Atlas' et 'GL'
    "INFO": [],       # Par exemple, pour INFO on exclut 'Startup'
    "WARNING": [],  # Pour WARNING, on exclut 'LowMemory'
    "ERROR": [],               # Aucune exclusion pour les erreurs
    "CRITICAL": []             # Aucune exclusion pour les erreurs critiques
}

# Filtre personnalisé pour exclure certains messages en fonction du niveau de log
class BlacklistFilter(logging.Filter):
    def filter(self, record):
        # Récupérer le niveau de log
        level = record.levelname

        # Si le niveau de log est dans le LOG_BLACKLIST, on vérifie les éléments à exclure
        if level in LOG_BLACKLIST:
            # Vérifier si le message contient un des éléments de la blacklist
            for item in LOG_BLACKLIST[level]:
                if item in record.getMessage():
                    return False  # Si trouvé, on ignore ce message
        return True  # Sinon, on garde le message

# Ajouter le filtre à tous les loggers kivy
Logger.setLevel('DEBUG')
kivy_logger = logging.getLogger('kivy')
kivy_logger.addFilter(BlacklistFilter())

from app.screens import TitleScreen, HomeScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

# Main Pong application class
class SportifyApp(App):
    def build(self):
        """Build the app interface."""
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(HomeScreen(name="home"))
        sm.current = 'title' # Actually Kivy take the first TitleScreen added has the first one so this line is not necessary
        Logger.debug(f"SpotifyApp: current Screen used : {sm.current}")

        return sm

# Run the application if this is the main script
if __name__ == '__main__':
    SportifyApp().run()  # Start the application

# Note from the dev :
# I will take kivy life or is kivy who will take my life first ?