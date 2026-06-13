"""Safe Standard Library - Wrapper aman untuk operasi sistem."""
import os as _os
import sys as _sys
import json as _json
import subprocess as _subprocess
import pickle as _pickle

class SafeOS:
    FORBIDDEN_PATHS = ['/etc/passwd', '/etc/shadow', '/etc/cron', '/root']
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

    @staticmethod
    def open(path, mode='r', *args, **kwargs):
        path = str(path)
        if '..' in path or '\x00' in path:
            raise ValueError(f"Path traversal/null byte: {path}")
        if path.startswith('/') and any(f in path for f in SafeOS.FORBIDDEN_PATHS):
            raise ValueError(f"Forbidden absolute path: {path}")
        # Gunakan built-in open agar mengembalikan file object
        return _os.fdopen(_os.open(path, _os.O_RDONLY if 'r' in mode else _os.O_WRONLY | _os.O_CREAT), mode, *args, **kwargs)

    @staticmethod
    def system(cmd):
        raise RuntimeError("os.system() is BLOCKED. Use SafeSubprocess.")

    @staticmethod
    def popen(*args, **kwargs):
        raise RuntimeError("os.popen() is BLOCKED. Use SafeSubprocess.")

    @staticmethod
    def path_join(*args):
        result = _os.path.join(*args)
        if '..' in result:
            raise ValueError(f"Path traversal in join: {result}")
        return result

    @staticmethod
    def listdir(path='.'):
        path = str(path)
        if '..' in path or path.startswith('/etc'):
            raise ValueError(f"Forbidden directory: {path}")
        return _os.listdir(path)

    @staticmethod
    def remove(path):
        path = str(path)
        if '..' in path or path.startswith('/'):
            raise ValueError(f"Cannot remove absolute path: {path}")
        return _os.remove(path)

    @staticmethod
    def environ(key, default=None):
        return _os.environ.get(key, default)

    @staticmethod
    def walk(top, topdown=True, onerror=None, followlinks=False):
        """Aman: hanya izinkan direktori yang tidak mengandung path traversal."""
        top = str(top)
        if '..' in top:
            raise ValueError(f"Path traversal in walk: {top}")
        for root, dirs, files in _os.walk(top, topdown, onerror, followlinks):
            # Filter direktori yang mengandung '..' (meskipun tidak mungkin)
            dirs[:] = [d for d in dirs if '..' not in d]
            yield root, dirs, files

    @staticmethod
    def path_isdir(p): return _os.path.isdir(str(p))
    @staticmethod
    def path_isfile(p): return _os.path.isfile(str(p))
    @staticmethod
    def path_exists(p): return _os.path.exists(str(p))
    @staticmethod
    def getcwd(): return _os.getcwd()

    @staticmethod
    def makedirs(path, exist_ok=True):
        path = str(path)
        if '..' in path or path.startswith('/'):
            raise ValueError(f"Forbidden path: {path}")
        return _os.makedirs(path, exist_ok=exist_ok)

class SafeSubprocess:
    ALLOWED_COMMANDS = {'ls', 'pwd', 'date', 'whoami', 'echo', 'cat'}

    @staticmethod
    def run(cmd, shell=False, **kwargs):
        import shlex
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        if cmd[0] not in SafeSubprocess.ALLOWED_COMMANDS:
            raise ValueError(f"Command not allowed: {cmd[0]}")
        if shell:
            raise ValueError("shell=True is BLOCKED")
        return _subprocess.run(cmd, shell=False, **kwargs)

class SafeJSON:
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB

    @staticmethod
    def loads(data, **kwargs):
        if len(data) > SafeJSON.MAX_SIZE:
            raise ValueError(f"JSON too large: {len(data)} bytes")
        return _json.loads(data, **kwargs)

    @staticmethod
    def load(fp, **kwargs):
        data = fp.read(SafeJSON.MAX_SIZE + 1)
        if len(data) > SafeJSON.MAX_SIZE:
            raise ValueError("JSON too large")
        return _json.loads(data, **kwargs)

    @staticmethod
    def dumps(obj, **kwargs):
        return _json.dumps(obj, **kwargs)

class SafePickle:
    @staticmethod
    def load(*args, **kwargs):
        raise RuntimeError("pickle.load() is BLOCKED.")
    @staticmethod
    def loads(*args, **kwargs):
        raise RuntimeError("pickle.loads() is BLOCKED.")
    @staticmethod
    def dump(*args, **kwargs):
        raise RuntimeError("pickle.dump() is BLOCKED.")

class SafeInput:
    MAX_LENGTH = 4096

    @staticmethod
    def input(prompt=''):
        user_input = input(prompt)
        if len(user_input) > SafeInput.MAX_LENGTH:
            raise ValueError(f"Input too long: {len(user_input)}")
        for c in ['\x00', '\r', '\n', '\x1b']:
            if c in user_input:
                raise ValueError(f"Dangerous character in input: {repr(c)}")
        return user_input

print("[+] Safe Library loaded!")
print("    SafeOS - File ops dengan validasi path")
print("    SafeSubprocess - Command dengan whitelist")
print("    SafeJSON - Parsing dengan size limit")
print("    SafePickle - DIBLOKIR TOTAL")
print("    SafeInput - Input dengan validasi")
