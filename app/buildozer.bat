@echo off
docker run --rm -it ^
  --volume "%cd%:/home/user/hostcwd" ^
  --volume "%USERPROFILE%\Desktop\.buildozer:/home/user/.buildozer" ^
  ghcr.io/kivy/buildozer:latest %*
