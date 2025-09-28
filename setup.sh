#-----Sys-Update-----#
echo "Updating The System"
sleep 3
paru -Syyu --noconfirm

#-----AUR-----#
echo "Installing AUR Packages"
sleep 3

paru -S --needed --noconfirm \
  swww \
  hyprshot \
	hypridle \
	hyprlock \
	hyprpicker \
  swaync \
	wl-clipboard \
  colorz \
	firefox \
  chromium \
  proton-authenticator-bin \
  sassc \
  bc \
  optipng \
  gtk-engine-murrine \
  meson \
  breeze-icons \
  code \
	nemo \
	nwg-look \
  gnome-disk-utility \
  nwg-displays \
	python-pywal16 \
	python-pywalfox \
	zsh \
  ttf-meslo-nerd \
  ttf-font-awesome \
	ttf-font-awesome-4 \
	ttf-font-awesome-5 \
	waybar \
	rust \
	cargo \
	fastfetch \
	cmatrix \
	pavucontrol \
  net-tools \
	waybar-module-pacman-updates-git \
  python-pillow \
  python-colorthief \
  python-haishoku \
  python-pystache \
  python-yaml \
	python-pip \
  python-psutil \
	python-virtualenv \
  python-requests \
  python-hijri-converter \
  python-pytz \
	python-gobject \
	xfce4-settings \
  xfce-polkit \
	exa \
	rofi-wayland \
  neovim \
  vulkan-tools \
  goverlay-git \
  flatpak \

#-----Flatpaks-----#

#echo "Installing FlatPaks....."
#sleep 3
flatpak install --noninteractive flathub com.bitwarden.desktop 
flatpak install --noninteractive flathub org.audacityteam.Audacity 
#flatpak install --noninteractive flathub org.libretro.RetroArch
#flatpak install --noninteractive flathub net.rpcs3.RPCS3

#-----Create-Directories-----#

echo "Creating Directories"
sleep 3
mkdir -p ~/git
mkdir -p ~/venv

#-----Updating-System-----#
echo "Checking For Updates For Newly Installed Packges"
sleep 3
paru -Syyu --noconfirm
#flatpak --noninteractive update

#-----Oh-My-Zsh-----#
echo "Installing Oh-My-Zsh"
sleep 3

mkdir -p /home/$USER/dots/omz

git clone "https://github.com/zsh-users/zsh-autosuggestions.git" "/home/$USER/dots/omz/zsh-autosuggestions/"
git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "/home/$USER/dots/omz/zsh-syntax-highlighting/"
git clone "https://github.com/zdharma-continuum/fast-syntax-highlighting.git" "/home/$USER/dots/omz/fast-syntax-highlighting/"
git clone --depth 1 -- "https://github.com/marlonrichert/zsh-autocomplete.git" "/home/$USER/dots/omz/zsh-autocomplete/"
git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "/home/$USER/dots/omz/autoswitch_virtualenv/"

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

rm -rf ~/.zshrc

cp -r /home/$USER/dots/omz/autoswitch_virtualenv/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/fast-syntax-highlighting/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-autocomplete/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-autosuggestions/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-syntax-highlighting/ ~/.oh-my-zsh/custom/plugins/

#-----Config-Symlink-----#
echo "Symlinking Configs"
sleep 3

rm -rf /home/$USER/dots/omz/
rm -rf /home/$USER/.config/hypr
rm -rf /home/$USER/.config/kitty
ln -s /home/$USER/dots/.zshrc /home/$USER/
ln -s /home/$USER/dots/fastfetch/ /home/$USER/.config/
ln -s /home/$USER/dots/gtk-3.0/ /home/$USER/.config/
ln -s /home/$USER/dots/gtk-4.0/ /home/$USER/.config/
ln -s /home/$USER/dots/hypr/ /home/$USER/.config/
ln -s /home/$USER/dots/swaync/ /home/$USER/.config/
ln -s /home/$USER/dots/kitty/ /home/$USER/.config/
ln -s /home/$USER/dots/nvim/ /home/$USER/.config/
ln -s /home/$USER/dots/rofi/ /home/$USER/.config/
ln -s /home/$USER/dots/scripts/ /home/$USER/.config/
ln -s /home/$USER/dots/waybar/ /home/$USER/.config/
ln -s /home/$USER/dots/.icons/ /home/$USER/
ln -s /home/$USER/dots/.themes/ /home/$USER/

echo "Symlinking Sys Configs"
sleep 3
sudo rm -rf /usr/share/icons/default
sudo cp -r /home/$USER/dots/sys/cursors/default /usr/share/icons/
sudo cp -r /home/$USER/dots/sys/cursors/Future-black-cursors /usr/share/icons/

sudo mkdir -p /usr/share/bg/
sudo cp -r /home/$USER/dots/sys/bg/bg.jpg /usr/share/bg/
sudo cp -r /home/$USER/dots/.icons/oomox-lightdm /usr/share/icons/
sudo cp -r /home/$USER/dots/.themes/oomox-lightdm /usr/share/themes/

#-----Apply-Theme-----#
echo "Applying Theme"
sleep 3

gsettings set org.gnome.desktop.interface cursor-theme "Future-black-cursors"
gsettings set org.gnome.desktop.interface icon-theme "oomox-Cachydepths5K"
gsettings set org.gnome.desktop.interface gtk-theme "oomox-Cachydepths5K"
gsettings set org.gnome.desktop.interface font-name "MesloLGL Nerd Font 12"
gsettings set org.gnome.desktop.interface document-font-name "MesloLGL Nerd Font 12"
gsettings set org.gnome.desktop.interface monospace-font-name "MesloLGL Mono Nerd Font 12"
gsettings set org.gnome.desktop.wm.preferences titlebar-font "MesloLGL Mono Nerd Font 12"
sudo cp -r /home/$USER/dots/sys/lightdm/ /etc/
cp -r ~/.config/hypr/bg/cachydepths5k.jpg ~/.config/hypr/bg/bg.jpg
swww-daemon
swww-img ~/.config/hypr/bg/bg.jpg
wal -i ~/.config/hypr/bg/bg.jpg --cols16

#-----Apply-GRUB-Theme-----#

echo "Please Choose Your GRUB Theme"
echo "You Can Have A Look At https://github.com/vinceliuice/Elegant-grub2-themes For The Previews !!!!"
sleep 5

cd ~/git/
git clone https://github.com/vinceliuice/Elegant-grub2-themes.git
cd Elegant-grub2-themes/
./install

echo "Installation Complete !!!"
echo "Rebooting The System"

sleep 3
sudo systemctl reboot
