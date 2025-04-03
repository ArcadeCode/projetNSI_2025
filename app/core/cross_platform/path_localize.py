from pathlib import Path
import os

from kivy.utils import platform

class PlatformNotSupportedException(Exception) :
    """Raised when the Platform is not supported by the application."""
    pass

def get_path_windows_linux() :
    path = Path(os.getcwd())
    return path

def get_path_android() :
    # TODO: Implement this function
    pass

SAVES_PATH = None

match platform:
    case "win":
        SAVES_PATH = get_path_windows_linux()
    case "linux":
        SAVES_PATH = get_path_windows_linux()
    case "macosx" :
        raise PlatformNotSupportedException("MACOSX is not supported by the program, please use other platform such as windows, linux or android.")
    case "android" :
        SAVES_PATH = get_path_android()
    case "ios" :
        raise PlatformNotSupportedException("IOS is not supported by the program, please use other platform such as windows, linux or android.")
    case _ : # Include when platform = "unknown"
        raise PlatformNotSupportedException("This platform is unknown.")