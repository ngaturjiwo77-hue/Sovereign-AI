import json, os
from kivy.app import App

class KnowledgeBase:
    def __init__(self, path="brain_knowledge.json"):
        # Arahkan ke folder data aplikasi yang diizinkan Android
        app = App.get_running_app()
        data_dir = app.user_data_dir if app else '.'
        self.path = os.path.join(data_dir, path)
        
        self.data = {
            "patterns": {}, "templates": {}, "vulnerabilities": {}, 
            "fixes": {}, "total_learned": 0
        }
        # Jangan load() paksa di sini jika file belum ada
        if os.path.exists(self.path):
            self.load()
    
    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except:
            pass

    def save(self):
        try:
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
        except:
            pass

    # ... (tambahkan fungsi lainnya seperti learn_from_code dan get_safe_template sesuai aslinya)
