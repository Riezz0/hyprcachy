#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import os
import subprocess
import shutil
import json
from pathlib import Path

class WallpaperSelector:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Wallpaper Selector")
        self.window.set_default_size(800, 600)
        self.window.set_border_width(10)
        
        # Wallpaper directory
        self.wallpaper_dir = os.path.expanduser("~/.config/hypr/bg/")
        self.bg_file = os.path.join(self.wallpaper_dir, "bg.jpg")
        self.theme_config_file = os.path.join(self.wallpaper_dir, "wallpaper_themes.json")
        
        # Load theme mapping from JSON file
        self.theme_mapping = self.load_theme_mapping()
        
        # Create main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(vbox)
        
        # Create title label
        title_label = Gtk.Label()
        title_label.set_markup("<b>Select Wallpaper</b>")
        vbox.pack_start(title_label, False, False, 0)
        
        # Create theme info label
        self.theme_info_label = Gtk.Label()
        self.theme_info_label.set_justify(Gtk.Justification.LEFT)
        vbox.pack_start(self.theme_info_label, False, False, 0)
        
        # Create scrolled window for thumbnails
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)
        
        # Create flow box for thumbnails
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_max_children_per_line(4)
        self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow_box.set_homogeneous(True)
        scrolled_window.add(self.flow_box)
        
        # Create apply button
        self.apply_button = Gtk.Button(label="Apply Wallpaper")
        self.apply_button.connect("clicked", self.on_apply_clicked)
        self.apply_button.set_sensitive(False)
        vbox.pack_start(self.apply_button, False, False, 0)
        
        # Create reload themes button
        self.reload_button = Gtk.Button(label="Reload Themes Config")
        self.reload_button.connect("clicked", self.on_reload_clicked)
        vbox.pack_start(self.reload_button, False, False, 0)
        
        # Connect signals
        self.flow_box.connect("child-activated", self.on_wallpaper_selected)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Load wallpapers
        self.load_wallpapers()
        
        # Store selected wallpaper path
        self.selected_wallpaper = None
    
    def load_theme_mapping(self):
        """Load theme mapping from JSON file"""
        default_themes = {
            "anime-room.jpg": {
                "gtk_theme": "oomox-anime_room",
                "icon_theme": "oomox-anime_room",
                "gtk4_theme": "oomox-anime_room"
            },
            "mountain.jpg": {
                "gtk_theme": "oomox-mountain", 
                "icon_theme": "oomox-mountain",
                "gtk4_theme": "oomox-mountain"
            },
            "sunset.jpg": {
                "gtk_theme": "oomox-sunset",
                "icon_theme": "oomox-sunset",
                "gtk4_theme": "oomox-sunset"
            }
        }
        
        try:
            if os.path.exists(self.theme_config_file):
                with open(self.theme_config_file, 'r') as f:
                    themes = json.load(f)
                    print(f"Loaded theme mapping from {self.theme_config_file}")
                    return themes
            else:
                # Create default config file if it doesn't exist
                with open(self.theme_config_file, 'w') as f:
                    json.dump(default_themes, f, indent=4)
                print(f"Created default theme config at {self.theme_config_file}")
                return default_themes
        except Exception as e:
            print(f"Error loading theme config: {e}. Using default themes.")
            return default_themes
    
    def on_reload_clicked(self, button):
        """Reload the theme configuration"""
        self.theme_mapping = self.load_theme_mapping()
        self.show_success("Theme configuration reloaded!")
        # Update theme info if a wallpaper is selected
        if hasattr(self, 'selected_filename'):
            self.update_theme_info(self.selected_filename)
    
    def get_theme_info(self, wallpaper_filename):
        """Get theme information for the selected wallpaper"""
        # Check exact filename match first
        if wallpaper_filename in self.theme_mapping:
            return self.theme_mapping[wallpaper_filename]
        
        # Check for partial matches (in case filenames have variations)
        for pattern, theme_info in self.theme_mapping.items():
            if pattern.lower() in wallpaper_filename.lower():
                return theme_info
        
        # Return default theme if no match found
        return {
            "gtk_theme": "Default",
            "icon_theme": "Default",
            "gtk4_theme": "Default"
        }
    
    def update_theme_info(self, wallpaper_filename):
        """Update the theme information label"""
        theme_info = self.get_theme_info(wallpaper_filename)
        
        theme_text = f"GTK Theme: {theme_info['gtk_theme']}\nIcon Theme: {theme_info['icon_theme']}\nGTK4 Theme: {theme_info['gtk4_theme']}"
        
        if theme_info['gtk_theme'] == "Default":
            theme_text += "\n\nNo specific theme configured for this wallpaper."
        else:
            theme_text += f"\n\nTheme configuration loaded from:\n{self.theme_config_file}"
        
        self.theme_info_label.set_text(theme_text)
    
    def copy_gtk4_theme(self, gtk4_theme_name):
        """Copy GTK-4.0 theme file to the config directory"""
        if gtk4_theme_name == "Default":
            print("No GTK4 theme to copy")
            return True
        
        try:
            # Source and destination paths
            source_path = os.path.expanduser(f"~/.themes/{gtk4_theme_name}/gtk-4.0/gtk.css")
            dest_dir = os.path.expanduser("~/.config/gtk-4.0/")
            dest_path = os.path.join(dest_dir, "gtk.css")
            
            # Check if source file exists
            if not os.path.exists(source_path):
                print(f"GTK4 theme file not found: {source_path}")
                return False
            
            # Create destination directory if it doesn't exist
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            print(f"Copied GTK4 theme: {source_path} -> {dest_path}")
            return True
            
        except Exception as e:
            print(f"Error copying GTK4 theme: {e}")
            return False
    
    def apply_gtk_themes(self, wallpaper_filename):
        """Apply GTK themes using gsettings and copy GTK4 theme files"""
        theme_info = self.get_theme_info(wallpaper_filename)
        
        # Skip if using default theme
        if theme_info['gtk_theme'] == "Default":
            print("No specific GTK theme configured for this wallpaper")
            return True
        
        theme_success = True
        
        try:
            # Apply GTK theme
            subprocess.run([
                "gsettings", "set", "org.gnome.desktop.interface", 
                "gtk-theme", theme_info['gtk_theme']
            ], check=True)
            print(f"Applied GTK theme: {theme_info['gtk_theme']}")
            
            # Apply icon theme
            subprocess.run([
                "gsettings", "set", "org.gnome.desktop.interface",
                "icon-theme", theme_info['icon_theme']
            ], check=True)
            print(f"Applied icon theme: {theme_info['icon_theme']}")
            
            # Copy GTK4 theme file
            gtk4_success = self.copy_gtk4_theme(theme_info['gtk4_theme'])
            if not gtk4_success:
                theme_success = False
                print(f"Warning: Could not copy GTK4 theme for {theme_info['gtk4_theme']}")
            
            return theme_success
            
        except subprocess.CalledProcessError as e:
            print(f"Error applying GTK themes: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error applying themes: {e}")
            return False
    
    def load_wallpapers(self):
        """Load wallpapers from directory, excluding bg.jpg"""
        try:
            # Clear existing thumbnails
            for child in self.flow_box.get_children():
                self.flow_box.remove(child)
            
            # Get image files
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
            wallpapers = []
            
            for file in os.listdir(self.wallpaper_dir):
                file_path = os.path.join(self.wallpaper_dir, file)
                if (os.path.isfile(file_path) and 
                    os.path.splitext(file.lower())[1] in image_extensions and
                    file != "bg.jpg"):
                    wallpapers.append(file_path)
            
            # Sort alphabetically
            wallpapers.sort()
            
            # Create thumbnails
            for wallpaper_path in wallpapers:
                self.create_thumbnail(wallpaper_path)
                
        except Exception as e:
            self.show_error(f"Error loading wallpapers: {e}")
    
    def create_thumbnail(self, wallpaper_path):
        """Create a thumbnail for the wallpaper"""
        try:
            # Create a box for each wallpaper
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            
            # Load and scale pixbuf
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(wallpaper_path, 200, 150)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            
            # Create label with filename
            filename = os.path.basename(wallpaper_path)
            label = Gtk.Label(label=filename)
            label.set_max_width_chars(20)
            label.set_ellipsize(True)
            
            vbox.pack_start(image, True, True, 0)
            vbox.pack_start(label, False, False, 0)
            
            # Create flow box child
            child = Gtk.FlowBoxChild()
            child.add(vbox)
            child.wallpaper_path = wallpaper_path  # Store path for later use
            child.filename = filename  # Store filename for theme lookup
            
            self.flow_box.add(child)
            
        except Exception as e:
            print(f"Error creating thumbnail for {wallpaper_path}: {e}")
    
    def on_wallpaper_selected(self, flow_box, child):
        """Handle wallpaper selection"""
        self.selected_wallpaper = child.wallpaper_path
        self.selected_filename = child.filename
        self.apply_button.set_sensitive(True)
        
        # Update theme information
        self.update_theme_info(child.filename)
    
    def on_apply_clicked(self, button):
        """Apply the selected wallpaper"""
        if not self.selected_wallpaper:
            return
        
        try:
            # Disable button during processing
            button.set_sensitive(False)
            button.set_label("Applying...")
            
            # Run operations in a thread to avoid freezing the UI
            GLib.idle_add(self.apply_wallpaper_operations)
            
        except Exception as e:
            self.show_error(f"Error applying wallpaper: {e}")
            button.set_sensitive(True)
            button.set_label("Apply Wallpaper")
    
    def apply_wallpaper_operations(self):
        """Perform all wallpaper application operations"""
        try:
            # 1. Copy selected wallpaper to bg.jpg
            shutil.copy2(self.selected_wallpaper, self.bg_file)
            print(f"Copied {self.selected_wallpaper} to {self.bg_file}")
            
            # 2. Apply GTK themes and copy GTK4 theme file
            theme_success = self.apply_gtk_themes(self.selected_filename)
            if not theme_success:
                self.show_warning("Wallpaper applied but there was an issue with GTK themes")
            
            # 3. Apply wallpaper with swww
            subprocess.run(["swww", "img", self.bg_file], check=True)
            print("Applied wallpaper with swww")
            
            # 4. Run wal to generate colors with --cols16 flag
            subprocess.run(["wal", "-i", self.bg_file, "--cols16"], check=True)
            print("Generated colors with wal --cols16")
            
            # 5. Copy color files
            home = os.path.expanduser("~")
            
            # Kitty colors
            kitty_src = os.path.join(home, ".cache/wal/colors-kitty.conf")
            kitty_dest = os.path.join(home, ".config/kitty/colors.conf")
            if os.path.exists(kitty_src):
                shutil.copy2(kitty_src, kitty_dest)
                print("Copied kitty colors")
            
            # Hyprland colors
            hypr_src = os.path.join(home, ".cache/wal/colors-hyprland.conf")
            hypr_dest = os.path.join(home, ".config/hypr/colors.conf")
            if os.path.exists(hypr_src):
                shutil.copy2(hypr_src, hypr_dest)
                print("Copied hyprland colors")
            
            # Waybar colors
            waybar_src = os.path.join(home, ".cache/wal/colors-waybar.css")
            waybar_dest = os.path.join(home, ".config/waybar/colors.css")
            if os.path.exists(waybar_src):
                shutil.copy2(waybar_src, waybar_dest)
                print("Copied waybar colors")
            
            # 6. Update pywalfox
            pywalfox_success = self.update_pywalfox()
            if not pywalfox_success:
                print("Warning: Pywalfox update failed")
            
            # 7. Restart waybar
            subprocess.run(["pkill", "waybar"])
            subprocess.Popen(["waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Restarted waybar")
            
            # 8. Reload hyprland
            subprocess.run(["hyprctl", "reload"])
            print("Reloaded hyprland")
            
            # 9. Reload kitty
            kitty_pids = subprocess.run(["pgrep", "kitty"], capture_output=True, text=True)
            if kitty_pids.stdout:
                for pid in kitty_pids.stdout.strip().split('\n'):
                    if pid:
                        subprocess.run(["kill", "-SIGUSR1", pid])
                print("Reloaded kitty")
            
            # Show success message
            success_message = "Wallpaper and themes applied successfully!"
            if not theme_success:
                success_message = "Wallpaper applied successfully! (Theme had minor issues)"
            if not pywalfox_success:
                success_message += " (Pywalfox update failed)"
            
            self.show_success(success_message)
            
        except subprocess.CalledProcessError as e:
            self.show_error(f"Command failed: {e}")
        except Exception as e:
            self.show_error(f"Error during wallpaper application: {e}")
        finally:
            # Re-enable button
            GLib.idle_add(self.reset_apply_button)
    
    def update_pywalfox(self):
        """Update pywalfox with the new color scheme"""
        try:
            subprocess.run(["pywalfox", "update"], check=True)
            print("Updated pywalfox")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error updating pywalfox: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error updating pywalfox: {e}")
            return False
    
    def reset_apply_button(self):
        """Reset the apply button state"""
        self.apply_button.set_sensitive(True)
        self.apply_button.set_label("Apply Wallpaper")
    
    def show_error(self, message):
        """Show error dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def show_warning(self, message):
        """Show warning dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def show_success(self, message):
        """Show success dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def run(self):
        """Show the window and start the application"""
        self.window.show_all()
        Gtk.main()

def main():
    # Check if required directories exist
    wallpaper_dir = os.path.expanduser("~/.config/hypr/bg/")
    if not os.path.exists(wallpaper_dir):
        print(f"Error: Wallpaper directory {wallpaper_dir} does not exist")
        return
    
    # Check if required commands are available
    required_commands = ['swww', 'wal', 'gsettings']
    optional_commands = ['pywalfox']
    
    for cmd in required_commands:
        if not shutil.which(cmd):
            print(f"Error: Required command '{cmd}' not found in PATH")
            return
    
    for cmd in optional_commands:
        if not shutil.which(cmd):
            print(f"Warning: Optional command '{cmd}' not found in PATH")
    
    # Run the application
    app = WallpaperSelector()
    app.run()

if __name__ == "__main__":
    main()
