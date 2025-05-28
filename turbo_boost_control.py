#!/usr/bin/env python3

# cSpell:ignore hexpand vexpand halign pkexec cpufreq

import gi
import subprocess
import psutil
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

NO_TURBO_PATH = "/sys/devices/system/cpu/intel_pstate/no_turbo"

class TurboBoostControl(Gtk.Window):
    def __init__(self):
        super().__init__(title="Turbo Boost Control")
        self.set_border_width(24)
        self.set_default_size(400, 200)
        self.set_resizable(False)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        vbox.set_homogeneous(False)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        self.add(vbox)

        # Turbo Boost Status
        self.status_label = Gtk.Label()
        self.status_label.set_justify(Gtk.Justification.CENTER)
        self.status_label.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(self.status_label, False, False, 0)

        # Buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        hbox.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(hbox, False, False, 0)

        self.disable_btn = Gtk.Button(label="Disable Turbo Boost")
        self.disable_btn.set_size_request(150, 40)
        self.disable_btn.connect("clicked", self.disable_turbo_boost)
        hbox.pack_start(self.disable_btn, False, False, 0)

        self.enable_btn = Gtk.Button(label="Enable Turbo Boost")
        self.enable_btn.set_size_request(150, 40)
        self.enable_btn.connect("clicked", self.enable_turbo_boost)
        hbox.pack_start(self.enable_btn, False, False, 0)

        # CPU Usage and Frequency
        self.usage_label = Gtk.Label()
        self.usage_label.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(self.usage_label, False, False, 0)

        self.freq_label = Gtk.Label()
        self.freq_label.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(self.freq_label, False, False, 0)

        # Start periodic update
        GLib.timeout_add_seconds(1, self.update_info)
        self.update_info()

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def get_turbo_status(self):
        try:
            with open(NO_TURBO_PATH, "r") as f:
                value = f.read().strip()
                if value == "0":
                    return True  # Turbo Boost enabled
                elif value == "1":
                    return False  # Turbo Boost disabled
                else:
                    return None
        except Exception:
            return None

    def enable_turbo_boost(self, button):
        self.status_label.set_text("Processing... (Enabling Turbo Boost)")
        self.enable_btn.set_sensitive(False)
        self.disable_btn.set_sensitive(False)
        result = subprocess.run([
            'pkexec', 'sh', '-c', f'echo 0 > {NO_TURBO_PATH}'
        ], capture_output=True, text=True)
        time.sleep(1)
        if result.returncode != 0:
            self.show_error(f"Failed to enable Turbo Boost.\n{result.stderr.strip()}")
        self.update_info()

    def disable_turbo_boost(self, button):
        self.status_label.set_text("Processing... (Disabling Turbo Boost)")
        self.enable_btn.set_sensitive(False)
        self.disable_btn.set_sensitive(False)
        result = subprocess.run([
            'pkexec', 'sh', '-c', f'echo 1 > {NO_TURBO_PATH}'
        ], capture_output=True, text=True)
        time.sleep(1)
        if result.returncode != 0:
            self.show_error(f"Failed to disable Turbo Boost.\n{result.stderr.strip()}")
        self.update_info()

    def update_info(self, *args):
        # Turbo Boost status
        turbo = self.get_turbo_status()
        if turbo is None:
            self.status_label.set_text("Turbo Boost: Unknown (Permission?)")
            self.enable_btn.set_sensitive(False)
            self.disable_btn.set_sensitive(False)
        elif turbo:
            self.status_label.set_text("Turbo Boost: ENABLED")
            self.enable_btn.set_sensitive(False)
            self.disable_btn.set_sensitive(True)
        else:
            self.status_label.set_text("Turbo Boost: DISABLED")
            self.enable_btn.set_sensitive(True)
            self.disable_btn.set_sensitive(False)

        # CPU usage and frequency
        try:
            usage = psutil.cpu_percent(interval=0)
            freq = psutil.cpu_freq()
            freq_str = f"{freq.current:.0f} MHz" if freq else "Unknown"
            self.usage_label.set_text(f"CPU Usage: {usage:.1f}%")
            self.freq_label.set_text(f"Current Frequency: {freq_str}")
        except Exception:
            self.usage_label.set_text("CPU Usage: Unknown")
            self.freq_label.set_text("Current Frequency: Unknown")

        return True

def main():
    win = TurboBoostControl()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main() 