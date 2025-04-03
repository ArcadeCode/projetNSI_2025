from app.screens import TitleScreen, HomeScreen
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

# Main Pong application class
class SportifyApp(App):
    def build(self):
        """Build the app interface."""
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(HomeScreen(name="home"))
        #return TitleScreenWidget()

# Run the application if this is the main script
if __name__ == '__main__':
    SportifyApp().run()  # Start the application
