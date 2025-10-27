#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk

# Constants
APP_ID = "com.warpcord.launcher"
CONFIG_DIR = Path.home() / ".config" / "warpcord"
CONFIG_FILE = CONFIG_DIR / "config.json"
DISCORD_PATH = "/opt/discord/Discord"

PROXY_TYPES = ["None", "SOCKS5", "HTTP"]
PROXY_SCHEMES = ["", "socks5", "http"]


class ProxyConfig:
    """Handle proxy configuration loading and saving."""

    def __init__(self, proxy_type: str = "None", ip: str = "", port: str = ""):
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port

    @classmethod
    def load(cls) -> "ProxyConfig":
        """Load configuration from file."""
        if not CONFIG_FILE.exists():
            return cls()

        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                proxy_type = data.get("proxy_type", "None")
                if proxy_type not in PROXY_TYPES:
                    proxy_type = "None"
                return cls(
                    proxy_type=proxy_type,
                    ip=data.get("ip", ""),
                    port=data.get("port", ""),
                )
        except (json.JSONDecodeError, OSError):
            return cls()

    def save(self) -> None:
        """Save configuration to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "proxy_type": self.proxy_type,
            "ip": self.ip,
            "port": self.port,
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def validate(self) -> Optional[str]:
        """Validate proxy configuration. Returns error message or None."""
        if self.proxy_type == "None":
            return None

        if not self.ip:
            return "IP address is required when a proxy is selected."

        if not self.port.isdigit():
            return "Port must be a valid number."

        port_num = int(self.port)
        if not (0 < port_num <= 65535):
            return "Port must be between 1 and 65535."

        return None

    def get_proxy_url(self) -> Optional[str]:
        """Get the proxy URL string, or None if no proxy."""
        if self.proxy_type == "None":
            return None

        idx = PROXY_TYPES.index(self.proxy_type)
        scheme = PROXY_SCHEMES[idx]
        return f"{scheme}://{self.ip}:{self.port}"


class WarpCordWindow(Adw.ApplicationWindow):
    """Main application window."""

    def __init__(self, app: Adw.Application):
        super().__init__(application=app)
        self.set_title("WarpCord")
        self.set_default_size(420, 200)

        self.config = ProxyConfig.load()
        self._build_ui()
        self._load_config_to_ui()

    def _build_ui(self) -> None:
        """Build the user interface."""
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=18,
            margin_bottom=18,
            margin_start=18,
            margin_end=18,
        )
        self.set_content(vbox)

        # Proxy type selection
        vbox.append(Gtk.Label(label="Proxy Type:", xalign=0))
        self.proxy_dropdown = Gtk.DropDown.new_from_strings(PROXY_TYPES)
        self.proxy_dropdown.connect("notify::selected", self._on_proxy_type_changed)
        vbox.append(self.proxy_dropdown)

        # IP and Port grid
        grid = Gtk.Grid(column_spacing=12, row_spacing=8)
        vbox.append(grid)

        grid.attach(Gtk.Label(label="IP Address:", xalign=0), 0, 0, 1, 1)
        self.ip_entry = Gtk.Entry()
        self.ip_entry.set_placeholder_text("127.0.0.1")
        self.ip_entry.set_hexpand(True)
        self.ip_entry.set_activates_default(True)
        grid.attach(self.ip_entry, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Port:", xalign=0), 0, 1, 1, 1)
        self.port_entry = Gtk.Entry()
        self.port_entry.set_placeholder_text("8080")
        self.port_entry.set_activates_default(True)
        grid.attach(self.port_entry, 1, 1, 1, 1)

        # Launch button
        self.launch_button = Gtk.Button(label="Warp Discord")
        self.launch_button.add_css_class("suggested-action")
        self.launch_button.connect("clicked", self._on_launch_clicked)
        vbox.append(self.launch_button)

        self.set_default_widget(self.launch_button)

    def _load_config_to_ui(self) -> None:
        """Load saved configuration into UI elements."""
        idx = PROXY_TYPES.index(self.config.proxy_type)
        self.proxy_dropdown.set_selected(idx)
        self.ip_entry.set_text(self.config.ip)
        self.port_entry.set_text(self.config.port)
        self._update_entry_sensitivity()

    def _on_proxy_type_changed(self, dropdown: Gtk.DropDown, _pspec) -> None:
        """Handle proxy type selection changes."""
        self._update_entry_sensitivity()

    def _update_entry_sensitivity(self) -> None:
        """Enable/disable IP and Port entries based on proxy type."""
        enabled = self.proxy_dropdown.get_selected() != 0
        self.ip_entry.set_sensitive(enabled)
        self.port_entry.set_sensitive(enabled)

    def _on_launch_clicked(self, _button: Gtk.Button) -> None:
        """Handle launch button click."""
        # Update config from UI
        self.config.proxy_type = PROXY_TYPES[self.proxy_dropdown.get_selected()]
        self.config.ip = self.ip_entry.get_text().strip()
        self.config.port = self.port_entry.get_text().strip()

        # Validate
        error = self.config.validate()
        if error:
            self._show_error(error)
            return

        # Save config
        try:
            self.config.save()
        except OSError as e:
            self._show_error(f"Failed to save configuration: {e}")
            return

        # Launch Discord
        if not self._launch_discord():
            return

        # Close the application
        self.get_application().quit()

    def _launch_discord(self) -> bool:
        """Launch Discord with proxy settings. Returns True on success."""
        cmd = [DISCORD_PATH]
        env = os.environ.copy()

        proxy_url = self.config.get_proxy_url()
        if proxy_url:
            env["http_proxy"] = proxy_url
            env["https_proxy"] = proxy_url
            cmd.append(f"--proxy-server={proxy_url}")

        try:
            subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except FileNotFoundError:
            self._show_error(f"Discord not found at {DISCORD_PATH}")
            return False
        except Exception as e:
            self._show_error(f"Failed to launch Discord: {e}")
            return False

    def _show_error(self, message: str) -> None:
        """Display an error dialog."""
        dialog = Adw.MessageDialog.new(self, message)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.set_close_response("ok")
        dialog.present()


class WarpCordApp(Adw.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

    def do_activate(self):
        """Handle application activation."""
        win = self.get_active_window()
        if not win:
            win = WarpCordWindow(self)
        win.present()


def main() -> int:
    """Application entry point."""
    app = WarpCordApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
