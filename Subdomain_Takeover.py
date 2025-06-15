import re
import requests 
import json 
import tabulate 

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"


FINGERPRINTS = {
    "GitHub Pages": "There isn't a GitHub Pages site here.",
    "Heroku": "No such app",
    "AWS S3": "NoSuchBucket",
    "Azure": "This web app has been stopped",
    "Fastly": "Fastly error: unknown domain"
}


def _fetch_response(domain):
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        response = r.text
        status_code = r.status_code
        return status_code, response
    
    except requests.RequestException as e:
        return None, str(e)

def _detect_takeover(response):
    for service, fingerprint in FINGERPRINTS.items():
        if fingerprint in response:
            return True, service
    return False, None

def check_subdomain_takeover(subdomain_file):
    with open(subdomain_file, "r") as file:
        subdomains = file.readlines()

        for sub in subdomains:
            sub = sub.strip()
            status_code, response = _fetch_response(sub)

            if status_code and response:
                vulnerable, service = _detect_takeover(response)
                if vulnerable:
                    print(f"{RED}[!] Potential Subdomain Takeover on {sub} via {service}{RESET}")
                else:
                    print(f"{GREEN}[-] {sub} seems safe.{RESET}")
            else:
                print(f"{RED}[x] Failed to connect to {sub}{RESET}")

if __name__ == "__main__":
    domain = "logitech.com"
    file = "subdomains.txt"
    check_subdomain_takeover(file)
