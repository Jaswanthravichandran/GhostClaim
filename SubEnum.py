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
        
        full_domain = f"{sub}.{self.domain}"
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

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [executor.submit(self._resolve_subdomain, sub) for sub in subdomains]            

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        self.found.append(result)
        except KeyboardInterrupt:
            print(f"{self.RED}[-] Interrupted by user. Exiting...{self.RESET}")
        except FileNotFoundError:
            print(f"{self.RED}[-] Wordlist not found: {self.wordlist_file}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}[-] Unexpected error: {e}{self.RESET}")
        
        return self.found 
    

    def save_to_file(self, filename='subdomains.txt'):
        try:
            with open(filename, "w") as file:
                for sub in self.found:
                    file.write(sub+"\n")
            print(f"\n{self.GREEN}[+] Saved {len(self.found)} subdomains to {filename}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}[-] Error writing to file: {e}{self.RESET}")