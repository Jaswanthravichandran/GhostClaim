import requests 

class SubdomainTakeover:

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

    def __init__(self, subdomain_file):
        self.subdomain_file = subdomain_file

    def _fetch_response(self, domain):
        try:
            r = requests.get(f"https://{domain}", timeout=5)
            response = r.text
            status_code = r.status_code
            return status_code, response
        
        except requests.RequestException as e:
            return None, str(e)

    def _detect_takeover(self, response):
        for service, fingerprint in self.FINGERPRINTS.items():
            if fingerprint in response:
                return True, service
        return False, None

    def check_subdomain_takeover(self):
        try:
            with open(self.subdomain_file, "r") as file:
                subdomains = file.readlines()

                for sub in subdomains:
                    sub = sub.strip()
                    print(f"{self.CYAN}[~] Scanning: {sub}{self.RESET}")
                    status_code, response = self._fetch_response(sub)

                    if status_code and response:
                        vulnerable, service = self._detect_takeover(response)
                        if vulnerable:
                            print(f"{self.RED}[!] Potential Subdomain Takeover on {sub} via {service}{self.RESET}")
                        else:
                            print(f"{self.GREEN}[-] {sub} seems safe.{self.RESET}")
                    else:
                        print(f"{self.RED}[x] Failed to connect to {sub}{self.RESET}")
        except FileNotFoundError:
            print(f"{self.RED}[-] Wordlist not found: {self.subdomain_file}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}[-] Unexpected error: {e}{self.RESET}")


