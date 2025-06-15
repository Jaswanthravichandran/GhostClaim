from SubEnum import SubdomainEnumerator
from Subdomain_Takeover import SubdomainTakeover

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"

if __name__ == "__main__":
    domain = "logitech.com"
    wordlist = "list.txt"
    file = "subdomains.txt"

    print(f"\n{YELLOW}[*] Starting Subdomain Enumeration...\n{RESET}")
    enum = SubdomainEnumerator(domain, wordlist, threads=30)
    enum.enumerate()
    enum.save_to_file()

    print(f"\n{YELLOW}[*] Starting Subdomain Takeover Check...\n{RESET}")
    takeover = SubdomainTakeover(file)
    takeover.check_subdomain_takeover()

"""
TODO:
    1.User Tool Options (argparser)
    2.Tool Symetics and Description
    3.Tool Setup Script
    4.Dockerise the tool 

"""
