#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.0"

import kivy
kivy.require('2.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import Screen, ScreenManager
import threading
import os
from pathlib import Path
import subprocess
import sys

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_downloading = False
        self.cancel_flag = False
        self.mode = "video"

        # Main Layout
        main = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main.canvas.before.clear()

        # Title
        title = Label(text='ELBASHA Downloader', size_hint_y=0.08, font_size='20sp', bold=True, color=(0,1,0,1))
        main.add_widget(title)

        # URL Section
        url_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        url_layout.add_widget(Label(text='URL:', size_hint_y=0.3, color=(0,1,0,1)))
        self.url_input = TextInput(multiline=False, size_hint_y=0.7, background_color=(0.1,0.1,0.15,1), foreground_color=(0,1,0,1))
        url_layout.add_widget(self.url_input)
        main.add_widget(url_layout)

        # Mode Selection
        mode_layout = GridLayout(cols=4, size_hint_y=0.08, spacing=5)
        mode_layout.add_widget(Label(text='Mode:', color=(0,1,0,1)))
        for text, mode_val in [("Video", "video"), ("Audio", "audio"), ("File", "file")]:
            btn = ToggleButton(text=text, group='mode', background_color=(0,0.7,0,1), color=(0,1,0,1))
            btn.mode_val = mode_val
            btn.bind(on_press=self.set_mode)
            mode_layout.add_widget(btn)
        main.add_widget(mode_layout)

        # Buttons
        btn_layout = GridLayout(cols=3, size_hint_y=0.08, spacing=5)
        paste_btn = Button(text='Paste', background_color=(0,1,0,1), color=(0,0,0,1))
        paste_btn.bind(on_press=self.paste_url)
        btn_layout.add_widget(paste_btn)

        clear_btn = Button(text='Clear', background_color=(0.8,0.1,0.1,1), color=(1,1,1,1))
        clear_btn.bind(on_press=self.clear_url)
        btn_layout.add_widget(clear_btn)

        folder_btn = Button(text='Folder', background_color=(0,0.5,1,1), color=(1,1,1,1))
        folder_btn.bind(on_press=self.open_folder)
        btn_layout.add_widget(folder_btn)
        main.add_widget(btn_layout)

        # Progress
        progress_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        progress_layout.add_widget(Label(text='Progress:', size_hint_y=0.3, color=(0,1,0,1)))
        self.progress_bar = ProgressBar(value=0, max=100, size_hint_y=0.35)
        progress_layout.add_widget(self.progress_bar)
        self.progress_label = Label(text='0%', size_hint_y=0.35, color=(0,1,0,1))
        progress_layout.add_widget(self.progress_label)
        main.add_widget(progress_layout)

        # Download Controls
        dl_layout = GridLayout(cols=2, size_hint_y=0.08, spacing=5)
        self.start_btn = Button(text='START', background_color=(0,0.7,0,1), color=(0,0,0,1), bold=True)
        self.start_btn.bind(on_press=self.start_download)
        dl_layout.add_widget(self.start_btn)

        self.stop_btn = Button(text='STOP', background_color=(0.7,0,0,1), color=(1,1,1,1), bold=True, disabled=True)
        self.stop_btn.bind(on_press=self.stop_download)
        dl_layout.add_widget(self.stop_btn)
        main.add_widget(dl_layout)

        # Status
        status_layout = BoxLayout(orientation='vertical', size_hint_y=0.35)
        status_layout.add_widget(Label(text='Status:', size_hint_y=0.1, color=(0,1,0,1)))
        scroll = ScrollView(size_hint_y=0.9)
        self.status = TextInput(multiline=True, readonly=True, background_color=(0.1,0.1,0.15,1), foreground_color=(0,1,0,1), text='Ready...')
        scroll.add_widget(self.status)
        status_layout.add_widget(scroll)
        main.add_widget(status_layout)

        self.add_widget(main)

    def set_mode(self, btn):
        if btn.state == 'down':
            self.mode = btn.mode_val
            self.log(f'Mode: {self.mode}')

    def paste_url(self, btn):
        try:
            url = Clipboard.paste()
            self.url_input.text = url
            self.log('URL pasted!')
        except:
            self.log('Error pasting URL')

    def clear_url(self, btn):
        self.url_input.text = ''
        self.log('URL cleared')

    def open_folder(self, btn):
        try:
            path = str(Path.home() / "Downloads")
            os.startfile(path)
        except:
            self.log('Could not open folder')

    def log(self, msg):
        self.status.text += f'\n[{msg}]'

    def start_download(self, btn):
        url = self.url_input.text.strip()
        if not url:
            self.log('ERROR: No URL provided')
            return

        self.is_downloading = True
        self.cancel_flag = False
        self.start_btn.disabled = True
        self.stop_btn.disabled = False

        thread = threading.Thread(target=self.download, args=(url,), daemon=True)
        thread.start()

    def stop_download(self, btn):
        self.cancel_flag = True
        self.log('Stopping download...')
        self.is_downloading = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

    def download(self, url):
        try:
            self.log(f'Starting download: {self.mode}')

            try:
                import yt_dlp
            except:
                self.log('Installing yt-dlp...')
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp', '-q'])
                import yt_dlp

            dl_path = str(Path.home() / 'Downloads')
            os.makedirs(dl_path, exist_ok=True)

            opts = {
                'outtmpl': os.path.join(dl_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }

            if self.mode == 'audio':
                opts['format'] = 'bestaudio/best'
                opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]
            else:
                opts['format'] = 'bestvideo+bestaudio/best'

            with yt_dlp.YoutubeDL(opts) as ydl:
                if not self.cancel_flag:
                    ydl.download([url])

            if not self.cancel_flag:
                self.log('SUCCESS! Download completed')
                self.progress_bar.value = 100
                self.progress_label.text = '100%'

        except Exception as e:
            if not self.cancel_flag:
                self.log(f'ERROR: {str(e)[:50]}')

        finally:
            self.is_downloading = False
            self.start_btn.disabled = False
            self.stop_btn.disabled = True

class ElbashaApp(App):
    def build(self):
        self.title = 'ELBASHA Downloader'
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    ElbashaApp().run()
