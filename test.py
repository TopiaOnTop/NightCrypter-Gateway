#!/usr/bin/env python3
import sys
import requests

DEFAULT_API_URL = "http://127.0.0.1:5000"

def main():
    print("=======================================")
    print("      dstat.topia Boom Test Script     ")
    print("=======================================")

    server = input("Entrez le nom du serveur (ex: Vantiva, GTT, OVH) : ").strip()
    if not server:
        print("Erreur: Le nom du serveur ne peut pas être vide.")
        sys.exit(1)

    print("\nFormat disponible :")
    print(" 1 : Drop (Pic de trafic puis zéro pendant 20 secondes)")
    print(" 2 : Continu (Pic continu approximatif à chaque fois)")
    fmt_input = input("Choisissez le format (1 ou 2) [défaut: 2] : ").strip()
    if fmt_input not in ['1', '2']:
        fmt = 2
    else:
        fmt = int(fmt_input)

    pps = input("Entrez les PPS (ex: 2500 MPPS, 500, 2.5M) [défaut: 2500] : ").strip()
    if not pps:
        pps = "2500"

    bps = input("Entrez le trafic / BPS (ex: 1500 Gbps, 15 Tbps, 500) [défaut: 1500] : ").strip()
    if not bps:
        bps = "1500"

    print(f"\n---> Envoi de la requête BOOM pour '{server}' (Format: {fmt}, PPS: {pps}, BPS: {bps})...")

    try:
        url = f"{DEFAULT_API_URL}/api/boom/{server}"
        payload = {
            "format": fmt,
            "pps": pps,
            "bps": bps
        }
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code == 200:
            print(f"Succès ! Réponse du serveur: {res.json().get('message')}")
        else:
            print(f"Erreur HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête BOOM: {e}")
        sys.exit(1)

    print("\nLe boom est en cours...")
    reset_choice = input("Appuyez sur Entrée ou tapez 'reset' (ou 'r') pour couper le boom / reset : ").strip().lower()

    try:
        reset_url = f"{DEFAULT_API_URL}/api/reset/{server}"
        res_reset = requests.post(reset_url, timeout=5)
        if res_reset.status_code == 200:
            print(f"Succès ! Boom coupé pour {server}: {res_reset.json().get('message')}")
        else:
            print(f"Erreur lors du reset: {res_reset.text}")
    except Exception as e:
        print(f"Erreur lors du reset: {e}")

if __name__ == '__main__':
    main()
