from app import APP_VERSION
from app.fonts import Font

from kivy.uix.label import Label

class VersionLabel(Label):
    '''Special Label who contain app version'''

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(VersionLabel, self).__init__(**kwargs)

        Label(text=f"version : {APP_VERSION}",
              font_size=12,
              font_name=Font.Montserrat_Bold,
              halign='center',
        )