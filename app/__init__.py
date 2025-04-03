# Open and reading version of app
with open('app/.version', 'r') as file:
    content = file.read()

APP_VERSION = content


import app.fonts
import app.core
import app.labels
import app.widgets