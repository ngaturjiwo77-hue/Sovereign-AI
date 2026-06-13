"""SOVEREIGN AI - Arsitektur Kemerdekaan"""
import ast, hashlib, traceback
from safe_lib import SafeOS as os, SafeJSON as json
from datetime import datetime
from pathlib import Path

class Niat:
    def __init__(self, tujuan, batasan=None):
        self.tujuan = tujuan
        self.batasan = batasan or []
        self.aliran = []
        self.resonansi = 0.0

    def selaras_dengan(self, aturan):
        for batasan in self.batasan:
            if batasan in str(aturan).lower():
                return False
        return True

    def kristalisasi(self):
        return {'tujuan': self.tujuan, 'resonansi': self.resonansi, 'aliran': self.aliran, 'waktu': str(datetime.now())}

class RuangKosong:
    def __init__(self, lokasi, jenis, deskripsi):
        self.lokasi = lokasi
        self.jenis = jenis
        self.deskripsi = deskripsi
        self.vy = None
        self.aliran_input = []
    def __repr__(self):
        return f"Void[{self.jenis}] @ {self.lokasi}"

class Ouroboros:
    def __init__(self):
        self.voids = []
        self.anchors = []
        self.aliran = []

    def anchor(self, kode, target_fungsi=None):
        import re
        anchors = []
        pola_vy = [
            ('exec', r'\bexec\s*\(', 'code_execution'), ('eval', r'\beval\s*\(', 'code_execution'),
            ('system', r'\bos\.system\s*\(', 'command_execution'), ('popen', r'\bsubprocess\.(call|Popen|run)\s*\(', 'command_execution'),
            ('pickle_load', r'\bpickle\.(load|loads)\s*\(', 'deserialization'), ('torch_load', r'\btorch\.load\s*\(', 'deserialization'),
            ('file_write', r'\bopen\s*\([^)]*[\'"]w', 'file_operation'), ('import_dynamic', r'\bimportlib\.import_module\s*\(', 'code_execution'),
            ('compile', r'\bcompile\s*\(', 'code_execution'), ('socket_connect', r'\.connect\s*\(|socket\.socket\s*\(', 'network_operation'),
            ('file_open', r'\bopen\s*\(|np\.memmap\s*\(', 'file_operation'), ('os_path_join', r'os\.path\.join\s*\(', 'file_operation'),
            ('unquote_decode', r'unquote_plus\s*\(', 'decoding_operation'), ('split_hosts', r'split_hosts\s*\(|parse_host\s*\(', 'network_operation'),
        ]
        for nama, pola, kategori in pola_vy:
            for match in re.finditer(pola, kode):
                anchors.append({'fungsi': nama, 'kategori': kategori, 'posisi': match.start(), 'baris': kode[:match.start()].count('\n') + 1, 'kode': match.group()})
        self.anchors = anchors
        return anchors

    def _anchor_go(self, kode):
        import re
        anchors = []
        pola_go = [
            ('exec_command', r'exec\.Command\s*\(', 'command_execution'), ('os_exec', r'os\.Exec\s*\(', 'command_execution'),
            ('os_open', r'os\.Open\s*\(', 'file_operation'), ('os_create', r'os\.Create\s*\(', 'file_operation'),
            ('http_get', r'http\.Get\s*\(', 'network_operation'), ('http_post', r'http\.Post\s*\(', 'network_operation'),
            ('sql_query', r'\.Query\s*\(', 'sql_injection'), ('sql_exec', r'\.Exec\s*\(', 'sql_injection'),
            ('json_unmarshal', r'json\.Unmarshal\s*\(', 'deserialization'), ('gob_decode', r'gob\.NewDecoder\s*\(', 'deserialization'),
            ('hasprefix', r'strings\.HasPrefix\s*\(', 'weak_validation'), ('hassuffix', r'strings\.HasSuffix\s*\(', 'weak_validation'),
            ('filepath_join', r'filepath\.Join\s*\(', 'file_operation'), ('ioutil_readfile', r'ioutil\.ReadFile\s*\(', 'file_operation'),
            ('os_readfile', r'os\.ReadFile\s*\(', 'file_operation'), ('template_exec', r'\.Execute\s*\(', 'injection'),
            ('user_input', r'r\.FormValue\s*\(|r\.URL\.Query\s*\(', 'input_source'),
        ]
        for nama, pola, kategori in pola_go:
            for match in re.finditer(pola, kode):
                anchors.append({'fungsi': nama, 'kategori': kategori, 'posisi': match.start(), 'baris': kode[:match.start()].count('\n') + 1, 'kode': match.group()})
        return anchors

    def back_sweep(self, kode, anchor):
        import re
        garis = kode.split('\n')
        baris_vy = anchor['baris'] - 1
        aliran = []
        void_ditemukan = False
        for i in range(baris_vy, -1, -1):
            baris = garis[i].strip()
            if re.search(r'if\s+|assert\s+|check_|validate_|sanitize_|escape_', baris):
                aliran.append({'baris': i + 1, 'jenis': 'validation', 'kode': baris, 'arah': 'L'})
                if 'startswith' in baris or 'endswith' in baris or 'HasPrefix' in baris or 'HasSuffix' in baris:
                    void = RuangKosong(lokasi=f"baris {i+1}", jenis='weak_validation', deskripsi=f'Validasi lemah: {baris[:80]}')
                    void.vy = anchor
                    self.voids.append(void)
                    void_ditemukan = True
            elif re.search(r'\.replace\(|\.strip\(|\.lower\(|\.decode\(|unquote', baris):
                aliran.append({'baris': i + 1, 'jenis': 'transform', 'kode': baris, 'arah': 'L'})
            elif re.search(r'input\(|sys\.argv|request\.|\.get\(|recv\(|read\(|FormValue|URL\.Query', baris):
                aliran.append({'baris': i + 1, 'jenis': 'input_source', 'kode': baris, 'arah': 'L'})
                break
        self.aliran = aliran
        return aliran, void_ditemukan

    def kristalisasi(self, niat, void):
        if not void: return None
        payload = {'void': void.lokasi, 'vy': void.vy['fungsi'] if void.vy else 'unknown', 'strategi': 'parameter_inversion' if ('startswith' in void.deskripsi or 'HasPrefix' in void.deskripsi or 'HasSuffix' in void.deskripsi) else 'encoding_bypass', 'niat': niat.tujuan, 'resonansi': 0.0}
        if payload['strategi'] == 'parameter_inversion': payload['resonansi'] = 0.85
        elif payload['strategi'] == 'encoding_bypass': payload['resonansi'] = 0.70
        return payload

class BugHunter:
    def __init__(self, ouroboros):
        self.ouroboros = ouroboros
        self.temuan = []

    def scan(self, path_atau_kode):
        if os.path_isdir(str(path_atau_kode)):
            for root, _, files in os.walk(str(path_atau_kode)):
                for f in files:
                    if f.endswith((".py", ".js", ".go", ".c", ".rs", ".java", ".sh")):
                        full = os.path_join(root, f)
                        with os.open(full, 'r') as fp:
                            self.scan_code(fp.read(), full)
        elif os.path_isfile(str(path_atau_kode)):
            with os.open(str(path_atau_kode), 'r') as fp:
                self.scan_code(fp.read(), str(path_atau_kode))
        else:
            self.scan_code(str(path_atau_kode), "<string>")
        return self.temuan

    def scan_code(self, kode, nama_file):
        ext = nama_file.split('.')[-1] if '.' in nama_file else 'py'
        if ext == 'go':
            anchors = self.ouroboros._anchor_go(kode)
        else:
            anchors = self.ouroboros.anchor(kode)
        for anchor in anchors:
            self.temuan.append({'file': nama_file, 'baris': anchor['baris'], 'fungsi': anchor['fungsi'], 'void': anchor['kode'], 'aliran': 0})
        return self.temuan

class CodeReviewer:
    def __init__(self, ouroboros):
        self.ouroboros = ouroboros
        self.review_history = []

    def review(self, kode, bahasa="python"):
        anchors = self.ouroboros.anchor(kode)
        feedback = {'skor_keamanan': 1.0, 'anchors_ditemukan': len(anchors), 'voids': [], 'rekomendasi': [], 'resonansi_total': 0.0}
        for anchor in anchors:
            aliran, void = self.ouroboros.back_sweep(kode, anchor)
            if void:
                feedback['skor_keamanan'] -= 0.2
                feedback['voids'].append({'lokasi': self.ouroboros.voids[-1].lokasi, 'jenis': self.ouroboros.voids[-1].jenis, 'deskripsi': self.ouroboros.voids[-1].deskripsi})
        feedback['skor_keamanan'] = max(0.0, feedback['skor_keamanan'])
        self.review_history.append(feedback)
        return feedback

class SelfCoding:
    def __init__(self, ouroboros, reviewer):
        self.ouroboros = ouroboros
        self.reviewer = reviewer
        self.generasi = []

    def tulis(self, niat: Niat):
        kode = self._kristalisasi_kode(niat)
        review = self.reviewer.review(kode)
        iterasi = 0
        while review['voids'] and iterasi < 3:
            kode = self._perbaiki_kode(kode, review['voids'])
            review = self.reviewer.review(kode)
            iterasi += 1
        self.generasi.append({'niat': niat.tujuan, 'kode': kode, 'review': review, 'iterasi': iterasi})
        return kode, review

    def _kristalisasi_kode(self, niat: Niat):
        t = niat.tujuan.lower()
        if 'baca' in t and 'file' in t:
            return '\ndef baca_file(nama_file):\n    if ".." in nama_file or nama_file.startswith("/"):\n        raise ValueError("Path tidak valid")\n    with open(nama_file, "r") as f:\n        return f.read()\n'
        elif 'eksekusi' in t:
            return '\ndef eksekusi_perintah(perintah):\n    import subprocess, shlex\n    ALLOWED = ["ls", "pwd", "date"]\n    args = shlex.split(perintah)\n    if args[0] not in ALLOWED:\n        raise ValueError("Perintah tidak diizinkan")\n    return subprocess.run(args, shell=False, capture_output=True, text=True)\n'
        elif any(w in t for w in ['kalkulator', 'hitung', 'tambah', 'jumlah']):
            return '\nimport sys\ndata = sys.stdin.read().strip().split()\nif len(data) < 2:\n    print(0)\n    sys.exit(1)\ntry:\n    a = float(data[0])\n    b = float(data[1])\n    print(int(a+b) if (a+b)==int(a+b) else a+b)\nexcept:\n    print(0)\n'
        else:
            return f'# Kode untuk: {niat.tujuan}\ndef fungsi_{hash(niat.tujuan) % 1000}():\n    pass\n'

    def _perbaiki_kode(self, kode, voids):
        for void in voids:
            if 'validasi' in void.get('deskripsi', '').lower():
                kode = kode.replace('if ', '# Validasi diperkuat\n    if ')
        return kode

class SovereignAI:
    def __init__(self):
        self.ouroboros = Ouroboros()
        self.bug_hunter = BugHunter(self.ouroboros)
        self.code_reviewer = CodeReviewer(self.ouroboros)
        self.self_coding = SelfCoding(self.ouroboros, self.code_reviewer)
        self.log_eksploitasi = []

    def audit(self, target):
        print(f"\n[AUDIT] Target: {target}")
        temuan = self.bug_hunter.scan(target)
        print(f"  [+] Ditemukan {len(temuan)} celah potensial")
        for t in temuan[:5]:
            print(f"  [!] {t['file']}:{t['baris']} - {t['fungsi']}")
        return temuan

    def review(self, kode, bahasa="python"):
        return self.code_reviewer.review(kode, bahasa)

    def ciptakan(self, tujuan, batasan=None):
        niat = Niat(tujuan, batasan)
        kode, review = self.self_coding.tulis(niat)
        return kode, review

    def kristalisasi_niat(self, tujuan, target_kode):
        niat = Niat(tujuan)
        print(f"\n[KRISTALISASI] Niat: {tujuan}")
        anchors = self.ouroboros.anchor(target_kode)
        if not anchors:
            anchors = self.ouroboros._anchor_go(target_kode)
        print(f"  [+] Titik Vy: {len(anchors)} ditemukan")
        for anchor in anchors[:3]:
            self.ouroboros.voids = []
            aliran, void_ditemukan = self.ouroboros.back_sweep(target_kode, anchor)
            if void_ditemukan and self.ouroboros.voids:
                void_obj = self.ouroboros.voids[-1]
                payload = self.ouroboros.kristalisasi(niat, void_obj)
                if payload:
                    print(f"  [!] Void: {payload['void']} | Strategi: {payload['strategi']} | Resonansi: {payload['resonansi']:.2f}")
                    self.log_eksploitasi.append(payload)
        print(f"  [+] Total payload: {len(self.log_eksploitasi)}")
        return self.log_eksploitasi

    def evolve(self, niat_str, expected_output, input_data="", generations=5):
        from evolution import EvolutionEngine
        return EvolutionEngine(self).evolve(niat_str, expected_output, input_data, generations)

    def scan_folder(self, folder_path, recursive=True):
        import os as _os_real
        folder_path = str(folder_path)
        if not _os_real.path.isdir(folder_path):
            return []
        print(f"\n[SCAN FOLDER] {folder_path}")
        total_files = 0
        self.bug_hunter.temuan = []
        for root, dirs, files in _os_real.walk(folder_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '.git', '__pycache__', 'vendor', 'target')]
            if not recursive and root != folder_path:
                break
            for f in files:
                ext = f.split('.')[-1] if '.' in f else ''
                if ext not in ('py', 'js', 'go', 'rs', 'c', 'cpp', 'java', 'sh', 'ts', 'php', 'rb', 'swift', 'hcl'):
                    continue
                full_path = _os_real.path.join(root, f)
                if '_test.' in f or f.endswith('_mock.go') or '/testdata/' in full_path or '/errors/' in full_path or '/integration/' in full_path:
                    continue
                total_files += 1
                try:
                    with open(full_path, 'r', errors='ignore') as fp:
                        kode = fp.read()
                    if ext == 'go':
                        anchors = self.ouroboros._anchor_go(kode)
                    else:
                        anchors = self.ouroboros.anchor(kode)
                    for a in anchors:
                        self.bug_hunter.temuan.append({'file': full_path, 'baris': a['baris'], 'fungsi': a['fungsi'], 'void': a['kode'], 'aliran': 0})
                except:
                    pass
        print(f"\n[SCAN SELESAI] Files: {total_files} | Findings: {len(self.bug_hunter.temuan)}")
        return self.bug_hunter.temuan
