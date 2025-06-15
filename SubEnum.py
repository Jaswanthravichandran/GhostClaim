#Subdomain Enumeration Module 

import requests
import dns.resolver 
from concurrent.futures import ThreadPoolExecutor, as_completed

class SubdomainEnumerator:

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, domain, wordlist_file, threads=20, timeout=2):
        self.domain = domain
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.found = []
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout

    def _resolve_subdomain(self, sub):
        sub = sub.strip()
        if not sub:
            return None 
        
        full_domain = f"{sub}.{domain}"
        try:
            self.resolver.resolve(full_domain, "A")
            print(f"{self.GREEN}[+] Domain Found {full_domain}{self.RESET}")
            return full_domain
        except(dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
            return None 

    def enumerate(self):
        try:
            with open(self.wordlist_file,'r') as file:
                        subdomains = file.readlines()
                        

def enum(domain, wordlist_file):
    resolver = dns.resolver.Resolver()
    found = []

    try:
        
                
    except KeyboardInterrupt:
        print(f"{RED}[-] Keybord Interrupt ! Exiting.....{RESET}")
        exit(0)
    except FileNotFoundError:
        print(f"{RED}[-] Wordlist file not found: {wordlist_file}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Unexpected error: {str(e)}{RESET}")

        file.close()
    
    for subs in found:
        try:
            with open('subdomains.txt', 'w') as file:
                for subs in found:
                    file.write(subs + '\n')
        except Exception as e:
            print(f"{RED}[-] Error saving subdomains: {e}{RESET}")

if __name__ == "__main__":
    domain = "logitech.com"
    wordlist_file = "list.txt"
    enum(domain, wordlist_file)