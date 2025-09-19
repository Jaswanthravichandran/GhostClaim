# Subdomain Enumeration Module

import dns.resolver
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm 

class SubdomainEnumerator:

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, domain, wordlist_file, threads=20, timeout=2, max_depth=2):
        self.domain = domain
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.max_depth = max_depth
        self.found = []
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout

    def _resolve_subdomain(self, fqdn):
        try:
            self.resolver.resolve(fqdn, "A")
            print(f"{self.GREEN}[+] Domain Found {fqdn}{self.RESET}")
            return fqdn
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
            return None

    def _generate_combinations(self, words):
        combinations = set()
        for depth in range(1, self.max_depth + 1):
            for combo in itertools.product(words, repeat=depth):
                sub = ".".join(combo)
                fqdn = f"{sub}.{self.domain}"
                combinations.add(fqdn)
        return list(combinations)

    def enumerate(self):
        try:
            with open(self.wordlist_file, 'r') as file:
                base_words = [line.strip() for line in file if line.strip()]

            candidates = self._generate_combinations(base_words)

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = {executor.submit(self._resolve_subdomain, fqdn): fqdn for fqdn in candidates}

                for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning", ncols=80):
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
                    file.write(sub + "\n")
            print(f"\n{self.GREEN}[+] Saved {len(self.found)} subdomains to {filename}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}[-] Error writing to file: {e}{self.RESET}")
