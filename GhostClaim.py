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
    domain = "example.com"
    wordlist = "list.txt"
    file = "subdomains.txt"
    log_file = "log.txt"
    vuln_file = "vulnerable-domains.txt"

    print(f"\n{YELLOW}[*] Starting Subdomain Enumeration...\n{RESET}")
    enum = SubdomainEnumerator(domain, wordlist, threads=256)
    enum.enumerate()
    enum.save_to_file()

    print(f"\n{YELLOW}[*] Starting Subdomain Takeover Check...\n{RESET}")
    takeover = SubdomainTakeover(file, log_file, vuln_file)
    takeover.check_subdomain_takeover()

"""
TODO:
    1.User Tool Options (argparser)
    2.Tool Symetics and Description
    3.Tool Setup Script
    4.Dockerise the tool 
    5.Add Domain Enumeration
    6.Let all the domains stored in the different files with it's subdomain list.
    7.Try to optimize the tool performance.
    8.In enumeration part check for both http & https.

"""
