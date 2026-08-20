#!/usr/bin/env python3
"""
dstat.topia API Client
A clean Python SDK and CLI tool to interact with the dstat.topia management API.
"""

import os
import sys
import argparse
import requests


class DstatAPIClient:
    """Client wrapper for interacting with dstat.topia Flask API endpoints."""

    def __init__(self, base_url="http://localhost:5000", api_token=None, admin_password=None):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.admin_password = admin_password

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["X-API-Token"] = self.api_token
        elif self.admin_password:
            headers["X-Admin-Password"] = self.admin_password
        return headers

    def get_servers(self):
        """Fetch all registered Layer 4 and Layer 7 target servers."""
        url = f"{self.base_url}/api/servers"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    def get_banners(self):
        """Fetch active banner advertisements."""
        url = f"{self.base_url}/api/banners"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    def get_reviews(self):
        """Fetch booter reviews list."""
        url = f"{self.base_url}/api/reviews"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    def trigger_layer4_boom(self, server=None, bandwidth="1500", packets="2500", mode=2):
        """
        Trigger Layer 4 graph metric simulation for a target server or globally.
        :param server: Server identifier (e.g. 'vantiva', 'gtt') or None for global
        :param bandwidth: Bandwidth value or string (e.g. '1500' or '1.5 Tbps')
        :param packets: Packets value or string (e.g. '2500' or '2.5 MPPS')
        :param mode: Format mode (2 = Continuous Peak, 1 = Peak then 20s Zero Drop)
        """
        endpoint = f"/api/boom/{server}" if server else "/api/boom"
        url = f"{self.base_url}{endpoint}"
        payload = {
            "bps": bandwidth,
            "pps": packets,
            "format": mode
        }
        response = requests.post(url, json=payload, headers=self._get_headers(), timeout=5)
        response.raise_for_status()
        return response.json()

    def trigger_layer7_boom(self, server=None, requests_per_sec="500000", mode=2):
        """
        Trigger Layer 7 RPS graph metric simulation for a target server or globally.
        :param server: Server identifier (e.g. 'fdcserver', 'vshield') or None for global
        :param requests_per_sec: RPS value or string (e.g. '500000' or '500k')
        :param mode: Format mode (2 = Continuous Peak, 1 = Peak then 20s Zero Drop)
        """
        endpoint = f"/api/boom/l7/{server}" if server else "/api/boom/l7"
        url = f"{self.base_url}{endpoint}"
        payload = {
            "rps": requests_per_sec,
            "format": mode
        }
        response = requests.post(url, json=payload, headers=self._get_headers(), timeout=5)
        response.raise_for_status()
        return response.json()

    def reset_boom(self, server=None, layer="l4"):
        """
        Reset active graph metric simulation.
        :param server: Server identifier or None for global reset
        :param layer: 'l4' or 'l7'
        """
        if layer == "l7":
            endpoint = f"/api/reset/l7/{server}" if server else "/api/reset/l7"
        else:
            endpoint = f"/api/reset/{server}" if server else "/api/reset"

        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self._get_headers(), timeout=5)
        response.raise_for_status()
        return response.json()


def main():
    parser = argparse.ArgumentParser(description="dstat.topia API Python Client")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of dstat instance")
    parser.add_argument("--token", help="API Token for authentication")
    parser.add_argument("--password", help="Admin Password for authentication")

    subparsers = parser.add_subparsers(dest="command", help="API Action Command")

    # Command: servers
    subparsers.add_parser("servers", help="List registered servers")

    # Command: boom-l4
    l4_parser = subparsers.add_parser("boom-l4", help="Trigger Layer 4 graph boom")
    l4_parser.add_argument("--server", help="Server name (e.g. vantiva)")
    l4_parser.add_argument("--bps", default="1500", help="Bandwidth (e.g. 1500 or 1.5 Tbps)")
    l4_parser.add_argument("--pps", default="2500", help="PPS (e.g. 2500 or 2.5 MPPS)")
    l4_parser.add_argument("--mode", type=int, default=2, choices=[1, 2], help="1=Drop, 2=Continuous")

    # Command: boom-l7
    l7_parser = subparsers.add_parser("boom-l7", help="Trigger Layer 7 graph boom")
    l7_parser.add_argument("--server", help="Server name (e.g. fdcserver)")
    l7_parser.add_argument("--rps", default="500000", help="Requests Per Second (e.g. 500k)")
    l7_parser.add_argument("--mode", type=int, default=2, choices=[1, 2], help="1=Drop, 2=Continuous")

    # Command: reset
    reset_parser = subparsers.add_parser("reset", help="Reset boom metrics")
    reset_parser.add_argument("--server", help="Server name")
    reset_parser.add_argument("--layer", choices=["l4", "l7"], default="l4", help="Layer type")

    args = parser.parse_args()

    client = DstatAPIClient(
        base_url=args.url,
        api_token=args.token or os.environ.get("DSTAT_API_TOKEN"),
        admin_password=args.password or os.environ.get("ADMIN_PASSWORD", "topiatheking")
    )

    if args.command == "servers":
        res = client.get_servers()
        print("Registered Servers:", res)
    elif args.command == "boom-l4":
        res = client.trigger_layer4_boom(server=args.server, bandwidth=args.bps, packets=args.pps, mode=args.mode)
        print("L4 Boom Response:", res)
    elif args.command == "boom-l7":
        res = client.trigger_layer7_boom(server=args.server, requests_per_sec=args.rps, mode=args.mode)
        print("L7 Boom Response:", res)
    elif args.command == "reset":
        res = client.reset_boom(server=args.server, layer=args.layer)
        print("Reset Response:", res)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
