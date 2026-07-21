import os
import sys
import json
import time
import subprocess
import threading
import webview
import psutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# ==========================================================================
# 1. CORE CRYTOGRAPHIC & SYSTEM OPERATIONS BACKEND (PYTHON API)
# ==========================================================================
class ProAPI:
    def __init__(self):
        # Dynamically derive 32-byte vault key using SHA-256 hash of the administrative gateway key "topiatheking"
        digest = hashes.Hash(hashes.SHA256())
        digest.update(b"topiatheking")
        self._vault_key = digest.finalize()
        self._aesgcm = AESGCM(self._vault_key)
        self._pgp_private_key = None
        self._pgp_public_key = None
        self.terminal_process = None
        self.terminal_thread = None

    # --- CRYPTOGRAPHIC SECURE FILE VAULT (AES-256 GCM) ---
    def vault_encrypt(self, file_path, dest_dir):
        try:
            if not os.path.exists(file_path):
                return {"status": "error", "message": "Source file does not exist"}

            with open(file_path, "rb") as f:
                data = f.read()

            nonce = os.urandom(12)
            ciphertext = self._aesgcm.encrypt(nonce, data, None)

            filename = os.path.basename(file_path)
            encrypted_data = nonce + ciphertext

            os.makedirs(dest_dir, exist_ok=True)
            encrypted_path = os.path.join(dest_dir, filename + ".vault")

            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)

            return {
                "status": "ok",
                "encrypted_path": encrypted_path,
                "message": f"Successfully encrypted and insulated file: {filename}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Encryption failed: {str(e)}"}

    def vault_decrypt(self, vault_path, dest_dir):
        try:
            if not os.path.exists(vault_path):
                return {"status": "error", "message": "Vault file does not exist"}

            with open(vault_path, "rb") as f:
                data = f.read()

            if len(data) < 12:
                return {"status": "error", "message": "Invalid vault file length"}

            nonce = data[:12]
            ciphertext = data[12:]
            decrypted_data = self._aesgcm.decrypt(nonce, ciphertext, None)

            filename = os.path.basename(vault_path).replace(".vault", "")
            os.makedirs(dest_dir, exist_ok=True)
            decrypted_path = os.path.join(dest_dir, filename)

            with open(decrypted_path, "wb") as f:
                f.write(decrypted_data)

            return {
                "status": "ok",
                "decrypted_path": decrypted_path,
                "message": f"Successfully decrypted and restored file: {filename}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Decryption failed: {str(e)}"}

    # --- XMR MONERO CRYPTO WALLET ENGINE ---
    def generate_xmr_wallet(self):
        try:
            # Seed words simulation list based on bip39
            words = ["oblivion", "secure", "quantum", "insulated", "private", "monero", "gateway", "vault",
                     "cryptography", "terminal", "darknet", "routing", "onion", "handshake", "entropy", "cipher"]
            import random
            seed_phrase = " ".join(random.sample(words, 12))

            # Simulated private view/spend key derivation
            view_key = "4" + os.urandom(31).hex()
            spend_key = "4" + os.urandom(31).hex()
            address = "44AFF" + os.urandom(45).hex()

            return {
                "status": "ok",
                "seed_phrase": seed_phrase,
                "view_key": view_key,
                "spend_key": spend_key,
                "address": address
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- PGP CRYPTOGRAPHY HANDLERS (RSA-2048) ---
    def generate_pgp_keypair(self):
        try:
            self._pgp_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self._pgp_public_key = self._pgp_private_key.public_key()
            return {"status": "ok", "message": "RSA-2048 Keypair successfully generated!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def pgp_encrypt(self, text):
        try:
            if not self._pgp_public_key:
                return {"status": "error", "message": "Generate PGP Keypair first"}

            ciphertext = self._pgp_public_key.encrypt(
                text.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return {"status": "ok", "encrypted": ciphertext.hex()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def pgp_decrypt(self, hex_ciphertext):
        try:
            if not self._pgp_private_key:
                return {"status": "error", "message": "Generate PGP Keypair first"}

            ciphertext = bytes.fromhex(hex_ciphertext)
            decrypted = self._pgp_private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return {"status": "ok", "decrypted": decrypted.decode('utf-8')}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- FILE SYSTEM OPERATIONS ---
    def read_dir(self, dir_path):
        try:
            resolved = os.path.abspath(dir_path)
            items = []
            for entry in os.scandir(resolved):
                items.append({
                    "name": entry.name,
                    "isDirectory": entry.is_dir(),
                    "path": entry.path
                })
            return {"status": "ok", "data": items, "current_path": resolved}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return {"status": "ok", "content": f.read()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_file(self, file_path, content):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def exists(self, file_path):
        return os.path.exists(file_path)

    def get_home_dir(self):
        return os.path.expanduser("~")

    # --- NATIVE EXECUTION WORKSPACE MANAGER ---
    def execute_binary(self, executable_path):
        try:
            # Spawn native executable subprocess
            subprocess.Popen([executable_path], shell=True)
            return {"status": "ok", "message": f"Successfully spawned binary instance: {os.path.basename(executable_path)}"}
        except Exception as e:
            return {"status": "error", "message": f"Execution failed: {str(e)}"}

    # --- TELEMETRY HARDWARE STATUS MONITOR ---
    def get_system_metrics(self):
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            return {
                "status": "ok",
                "cpu": int(cpu),
                "ramPercent": int(memory.percent),
                "ramUsed": f"{memory.used / (1024**3):.2f}",
                "ramTotal": f"{memory.total / (1024**3):.2f}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- INTERACTIVE TERMINAL EMULATOR ---
    def init_terminal(self):
        try:
            shell = "cmd.exe" if sys.platform == "win32" else "bash"
            self.terminal_process = subprocess.Popen(
                [shell],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Redirect stderr to stdout to prevent unread pipe deadlocks
                shell=True,
                text=True,
                bufsize=1
            )
            # Listen to outputs in separate thread
            self.terminal_thread = threading.Thread(target=self._stream_terminal_output, daemon=True)
            self.terminal_thread.start()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_terminal(self, command):
        if self.terminal_process and self.terminal_process.stdin:
            self.terminal_process.stdin.write(command + "\n")
            self.terminal_process.stdin.flush()

    def _stream_terminal_output(self):
        while self.terminal_process:
            line = self.terminal_process.stdout.readline()
            if not line:
                break
            # Stream back to frontend using pywebview Javascript bridge
            try:
                js_command = f"window.OS.appendTerminalOutput({json.dumps(line)});"
                webview.windows[0].evaluate_js(js_command)
            except:
                pass


# ==========================================================================
# 2. MONOLITHIC PYWEBVIEW THREAD RUNNER
# ==========================================================================
def main():
    api = ProAPI()
    # Create the virtual desktop native overlay window
    window = webview.create_window(
        title="Oblivion OS Monolith",
        url="index.html",
        js_api=api,
        width=1280,
        height=800,
        fullscreen=False,
        frameless=False
    )
    webview.start(debug=True)

if __name__ == '__main__':
    main()
