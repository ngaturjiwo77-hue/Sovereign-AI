from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import sys
import os
sys.path.insert(0, '.')

class SovereignApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20)
        self.label = Label(text="Sovereign AI Inisialisasi...")
        self.layout.add_widget(self.label)
        Clock.schedule_once(self.load_ai, 0.5)
        return self.layout

    def load_ai(self, dt):
        try:
            from sovereign_ai import SovereignAI
            self.ai = SovereignAI()
            self.label.text = "AI Berhasil Dimuat!"
        except Exception as e:
            self.label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    SovereignApp().run()
