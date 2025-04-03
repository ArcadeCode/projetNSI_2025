#!/bin/sh
docker run --rm -it \
  --volume "$(pwd):/home/user/hostcwd" \
  --volume "$HOME/Desktop/.buildozer:/home/user/.buildozer" \
  ghcr.io/kivy/buildozer:latest "$@"
