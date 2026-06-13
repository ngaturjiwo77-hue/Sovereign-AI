from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform  # TAMBAHKAN INI: Untuk mendeteksi Android
import threading
import sys
sys.path.insert(0, '.')
from sovereign_ai import SovereignAI

class SovereignApp(App):
    def build(self):
        # ==========================================
        # TAMBAHKAN BLOK INI UNTUK IZIN ANDROID
        # ==========================================
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])
        # ==========================================

        self.ai = SovereignAI()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        # Title
        layout.add_widget(Label(text='SOVEREIGN AI', font_size=24, bold=True, size_hint=(1, 0.05), color=(0, 1, 0.2, 1)))
        
        # ... (sisa kode layout kamu di bawahnya tetap sama) ...
        
        # Mode selector
        self.mode = Spinner(text='Audit Kode', values=['Audit Kode', 'Review Kode', 'Scan Folder', 'Create Code', 'Kristalisasi'], size_hint=(1, 0.06))
        layout.add_widget(self.mode)
        
        # Input
        self.input = TextInput(hint_text='Tempel kode atau path folder di sini...', size_hint=(1, 0.4), background_color=(0.05, 0.05, 0.05, 1), foreground_color=(0, 1, 0.2, 1))
        layout.add_widget(self.input)
        
        # Run button
        btn = Button(text='▶ JALANKAN', size_hint=(1, 0.06), background_color=(0, 0.8, 0.2, 1))
        btn.bind(on_press=self.run)
        layout.add_widget(btn)
        
        # Output
        self.output = Label(text='[Output muncul di sini]', size_hint=(1, 0.4), halign='left', valign='top', color=(0, 1, 0.2, 1))
        self.output.bind(size=self.output.setter('text_size'))
        scroll = ScrollView(size_hint=(1, 0.4))
        scroll.add_widget(self.output)
        layout.add_widget(scroll)
        
        return layout
    
    def run(self, instance):
        self.output.text = 'Processing...'
        def task():
            mode = self.mode.text
            data = self.input.text.strip()
            try:
                if mode == 'Audit Kode':
                    hasil = self.ai.audit(data)
                    Clock.schedule_once(lambda dt: setattr(self.output, 'text', f'Ditemukan {len(hasil)} celah'))
                elif mode == 'Review Kode':
                    hasil = self.ai.review(data)
                    Clock.schedule_once(lambda dt: setattr(self.output, 'text', f"Skor: {hasil['skor_keamanan']:.2f} | Anchors: {hasil['anchors_ditemukan']} | Voids: {len(hasil['voids'])}"))
                elif mode == 'Scan Folder':
                    hasil = self.ai.scan_folder(data)
                    Clock.schedule_once(lambda dt: setattr(self.output, 'text', f'Files scanned | Findings: {len(hasil)}'))
                elif mode == 'Create Code':
                    kode, review = self.ai.ciptakan(data)
                    Clock.schedule_once(lambda dt: setattr(self.output, 'text', kode))
                elif mode == 'Kristalisasi':
                    hasil = self.ai.kristalisasi_niat('exploit', data)
                    Clock.schedule_once(lambda dt: setattr(self.output, 'text', f'Payload: {len(hasil)}'))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.output, 'text', f'Error: {str(e)}'))
        threading.Thread(target=task).start()

if __name__ == '__main__':
    SovereignApp().run()
