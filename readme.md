# Oblivion OS Monolith - Insulated Cyber Virtual Desktop

Oblivion OS Monolith is an ultra-fluid, professional-grade virtual operating system environment constructed using **Pywebview**, **Python**, and a custom-crafted glassmorphism frontend. It strips away standard browser capabilities and runs inside a secure local sandbox with advanced encryption layers, a multi-threaded terminal, PGP tools, Monero wallets, and an integrated Tor onion routing browser.

---

## Key Architectural Advantages & Features

1. **Integrated Python Monolith (`main.py`):**
   - Serves both the backend systems API and embeds the raw glassmorphism frontend as an insulated data-stream string. One file to run everything with zero external build artifacts.
2. **Tor Network Onion Browser:**
   - Pre-routed MODE that encourages direct connection and surfing on onion nodes (such as DuckDuckGo Onion engine). Fully isolated from standard non-encrypted browsers.
3. **AES-256 GCM Secure Vault:**
   - Direct integration of symmetric Authenticated Encryption with Associated Data (AEAD) standard using AES-256 GCM. Users can import absolute disk files, symmetrically encrypt them into secure `.vault` insulated files, and restore them upon challenge request.
4. **Monero Wallet Sandbox:**
   - Real key derivation and seed phrase validation dashboard, validating spend keys, view keys, and addressing keys.
5. **PGP Cryptography Sandbox:**
   - Complete asymmetric RSA-2048 keypair generation, public key message encryption, and private key decrypting sandbox.
6. **Shell Terminal Link:**
   - Multi-threaded terminal process link communicating directly over standard shell.
7. **Mac Traffic Lights & Responsive Windows:**
   - Clean window dragging and coordinates-targeted GSAP Vacuum Genie minimize animations.

---

## Turnkey Installation & Boot Instructions

To run Oblivion OS, ensure you have Python 3.10+ installed on your host system.

### 1. Install Necessary System Dependencies
Install pywebview and the necessary cryptography modules:
```bash
pip install pywebview cryptography psutil
```

### 2. Boot the virtual Environment
Run the main script directly:
```bash
python main.py
```

### 3. Log In Credentials
Upon booting, authenticate using the authorized administrative credential keys:
- **Authorized User:** `Topia`
- **Symmetric Key:** `topiatheking`

---

## Encryption Security Details

### AES-256 GCM File Encryption
Files are symmetrically encrypted with a 32-byte master key using authenticated AES-GCM mode. When you click **Encrypt to Vault**, the backend:
1. Generates a cryptographically secure random 12-byte initialization vector (nonce).
2. Symmetrically encrypts the file byte-stream.
3. Prefixes the 12-byte nonce to the ciphertext and writes it as a `.vault` file into the target directory.
4. Safe extraction deletes the source file and retains the encrypted envelope.

### PGP Asymmetric Keypair
Keys are generated using standard RSA 2048-bit keys:
- Padding utilizes OAEP with a SHA-256 message digest and MGF1 mask generation. This prevents standard cipher vulnerabilities.

---

## Professional Operations Disclaimer
This system is created as a secure virtual sandbox. Keep your keys backed up. Oblivion OS Monolith provides end-to-end sandbox insulation to satisfy expert systems requirements.
