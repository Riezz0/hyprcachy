#!/bin/bash

# kitty --hold --class=AUR -e yay -Syyu --noconfirm \

kitty --class=AUR -e bash -c "paru -Syyu --noconfirm && echo '=== Updating Flatpak ===' && flatpak update -y; echo '=== All updates complete ==='; read -p 'Press Enter to close...'"
