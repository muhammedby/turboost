#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import os
import subprocess
import psutil
import threading
import time

class TurboBoostControl(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Intel Turbo Boost Kontrol")
        self.set_border_width(10)
        self.set_default_size(400, 300)
        self.set_resizable(False)
        
        # Ana container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Başlık
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Intel Turbo Boost Kontrol</span>")
        title_label.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(title_label, False, True, 10)
        
        # Durum bilgisi
        self.status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.status_icon = Gtk.Image()
        self.status_label = Gtk.Label()
        self.status_box.pack_start(self.status_icon, False, True, 0)
        self.status_box.pack_start(self.status_label, False, True, 0)
        main_box.pack_start(self.status_box, False, True, 10)
        
        # Kontrol butonları
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        
        self.enable_button = Gtk.Button(label="Turbo Boost'u Aç")
        self.enable_button.set_image(Gtk.Image.new_from_icon_name("gtk-apply", Gtk.IconSize.BUTTON))
        self.enable_button.connect("clicked", self.enable_turbo_boost)
        
        self.disable_button = Gtk.Button(label="Turbo Boost'u Kapat")
        self.disable_button.set_image(Gtk.Image.new_from_icon_name("gtk-cancel", Gtk.IconSize.BUTTON))
        self.disable_button.connect("clicked", self.disable_turbo_boost)
        
        button_box.pack_start(self.enable_button, False, True, 0)
        button_box.pack_start(self.disable_button, False, True, 0)
        main_box.pack_start(button_box, False, True, 10)
        
        # CPU bilgileri
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.cpu_info_label = Gtk.Label()
        self.cpu_freq_label = Gtk.Label()
        info_box.pack_start(self.cpu_info_label, False, True, 0)
        info_box.pack_start(self.cpu_freq_label, False, True, 0)
        main_box.pack_start(info_box, False, True, 10)
        
        # Durum güncelleme thread'i
        self.update_thread = threading.Thread(target=self.update_status, daemon=True)
        self.update_thread.start()
        
        # İlk durum kontrolü
        self.check_turbo_boost_status()
        
    def check_turbo_boost_status(self):
        try:
            with open("/sys/devices/system/cpu/intel_pstate/no_turbo", "r") as f:
                status = f.read().strip()
                if status == "1":
                    self.status_icon.set_from_icon_name("gtk-cancel", Gtk.IconSize.BUTTON)
                    self.status_label.set_markup("<span color='red'>Turbo Boost: Kapalı</span>")
                else:
                    self.status_icon.set_from_icon_name("gtk-apply", Gtk.IconSize.BUTTON)
                    self.status_label.set_markup("<span color='green'>Turbo Boost: Açık</span>")
        except:
            self.status_icon.set_from_icon_name("gtk-dialog-error", Gtk.IconSize.BUTTON)
            self.status_label.set_markup("<span color='orange'>Durum kontrol edilemiyor</span>")
    
    def enable_turbo_boost(self, button):
        try:
            subprocess.run(["pkexec", "sh", "-c", "echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo"], check=True)
            self.check_turbo_boost_status()
        except:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Hata"
            )
            dialog.format_secondary_text("Turbo Boost açılamadı. Lütfen root yetkisiyle çalıştırdığınızdan emin olun.")
            dialog.run()
            dialog.destroy()
    
    def disable_turbo_boost(self, button):
        try:
            subprocess.run(["pkexec", "sh", "-c", "echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo"], check=True)
            self.check_turbo_boost_status()
        except:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Hata"
            )
            dialog.format_secondary_text("Turbo Boost kapatılamadı. Lütfen root yetkisiyle çalıştırdığınızdan emin olun.")
            dialog.run()
            dialog.destroy()
    
    def update_status(self):
        while True:
            try:
                cpu_info = psutil.cpu_freq()
                cpu_count = psutil.cpu_count()
                cpu_percent = psutil.cpu_percent()
                
                GLib.idle_add(self.cpu_info_label.set_markup,
                    f"<span>CPU Kullanımı: {cpu_percent}%</span>")
                GLib.idle_add(self.cpu_freq_label.set_markup,
                    f"<span>CPU Frekansı: {cpu_info.current:.1f} MHz</span>")
                
                GLib.idle_add(self.check_turbo_boost_status)
            except:
                pass
            time.sleep(1)

if __name__ == "__main__":
    win = TurboBoostControl()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main() 