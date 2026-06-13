"""Knowledge base - menyimpan hasil belajar AI untuk referensi create kode."""
import json, os

class KnowledgeBase:
    def __init__(self, path="brain_knowledge.json"):
        self.path = path
        self.data = {
            "patterns": {},
            "templates": {},
            "vulnerabilities": {},
            "fixes": {},
            "total_learned": 0
        }
        self.load()
    
    def learn_from_code(self, code, language, anchors, voids):
        self.data["total_learned"] += 1
        for a in anchors:
            key = f"{a['fungsi']}_{a['kategori']}"
            if key not in self.data["patterns"]:
                self.data["patterns"][key] = {"count": 0, "examples": [], "safe_alternatives": []}
            self.data["patterns"][key]["count"] += 1
        for v in voids:
            vtype = v.get('jenis', 'unknown')
            if vtype not in self.data["vulnerabilities"]:
                self.data["vulnerabilities"][vtype] = {"count": 0}
            self.data["vulnerabilities"][vtype]["count"] += 1
        self.save()
    
    def get_safe_template(self, intention):
        i = intention.lower()
        # Match lebih fleksibel
        if any(w in i for w in ('upload', 'unggah', 'file')):
            if 'validasi' in i or 'aman' in i or 'safe' in i:
                return self.data["templates"].get("unrestricted_upload", None)
        if any(w in i for w in ('api', 'token', 'secret', 'key', 'kredensial')):
            return self.data["templates"].get("hardcoded_secret", None)
        if any(w in i for w in ('url', 'fetch', 'request', 'http', 'ambil')):
            return self.data["templates"].get("ssrf", None)
        if any(w in i for w in ('baca', 'read', 'load', 'buka')):
            return self._safe_read_template()
        if any(w in i for w in ('eksekusi', 'exec', 'run', 'jalankan', 'cmd')):
            return self._safe_exec_template()
        if any(w in i for w in ('simpan', 'save', 'write', 'tulis')):
            return self._safe_write_template()
        if any(w in i for w in ('query', 'sql', 'database', 'cari')):
            return self.data["templates"].get("sql_injection", None)
        if any(w in i for w in ('acak', 'random', 'token', 'generate')):
            return self.data["templates"].get("insecure_random", None)
        if any(w in i for w in ('tampil', 'xss', 'html', 'web')):
            return self.data["templates"].get("xss_injection", None)
        # Fallback original
        if 'baca' in i or 'read' in i:
            return '''def baca_file(nama_file):
    if '..' in nama_file or nama_file.startswith('/'):
        raise ValueError("Path tidak valid")
    with open(nama_file, 'r') as f:
        return f.read()'''
        elif 'eksekusi' in intention.lower() or 'exec' in intention.lower():
            return '''def eksekusi(perintah):
    import subprocess, shlex
    ALLOWED = {'ls', 'pwd', 'date'}
    args = shlex.split(perintah)
    if args[0] not in ALLOWED:
        raise ValueError("Tidak diizinkan")
    return subprocess.run(args, shell=False, capture_output=True, text=True)'''
        return None
    
    def get_learned_summary(self):
        return {
            "total_files": self.data["total_learned"],
            "patterns_known": len(self.data["patterns"]),
            "vulnerabilities_found": sum(v["count"] for v in self.data["vulnerabilities"].values()),
            "templates_available": list(self.data["templates"].keys()),
            "top_patterns": sorted(self.data["patterns"].items(), key=lambda x: x[1]["count"], reverse=True)[:5]
        }
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.data.update(json.load(f))
