from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import sys, threading, os

# Pastikan semua file terbaca
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SovereignApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Header
        self.layout.add_widget(Label(text='SOVEREIGN AI COMMAND CENTER', size_hint=(1, 0.08), bold=True, color=(0, 1, 0.5, 1)))
        
        # Control Panel
        self.mode = Spinner(text='Audit Kode', values=['Audit Kode', 'Review Kode', 'Scan Folder', 'Create Code', 'Kristalisasi'], size_hint=(1, 0.08))
        self.layout.add_widget(self.mode)
        
        self.input = TextInput(hint_text='Masukkan path folder atau source code...', size_hint=(1, 0.25), multiline=True)
        self.layout.add_widget(self.input)
        
        self.btn = Button(text='EXECUTE', size_hint=(1, 0.1), background_color=(0, 0.8, 0, 1))
        self.btn.bind(on_press=self.run_logic)
        self.layout.add_widget(self.btn)
        
        # Output Area
        self.scroll = ScrollView(size_hint=(1, 0.45))
        self.output = Label(text='Sistem Siap...', valign='top', halign='left', size_hint_y=None)
        self.output.bind(texture_size=lambda instance, value: setattr(instance, 'size', value))
        self.scroll.add_widget(self.output)
        self.layout.add_widget(self.scroll)
        
        Clock.schedule_once(self.load_ai, 0.1)
        return self.layout

    def load_ai(self, dt):
        try:
            from sovereign_ai import SovereignAI
            self.ai = SovereignAI()
            self.output.text = "Engine Loaded Successfully."
        except Exception as e:
            self.output.text = f"Init Error: {str(e)}"

    def run_logic(self, instance):
        threading.Thread(target=self.execute).start()

    def execute(self):
        cmd = self.mode.text
        data = self.input.text
        try:
            res = "Processing..."
            if cmd == 'Audit Kode': res = str(self.ai.audit(data))
            elif cmd == 'Review Kode': res = str(self.ai.review(data))
            elif cmd == 'Scan Folder': res = str(self.ai.scan_folder(data))
            elif cmd == 'Create Code': res = str(self.ai.ciptakan(data)[0])
            elif cmd == 'Kristalisasi': res = str(self.ai.kristalisasi_niat('exploit', data))
            
            Clock.schedule_once(lambda dt: setattr(self.output, 'text', res))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.output, 'text', f"Execution Error: {str(e)}"))

if __name__ == '__main__':
    SovereignApp().run()
