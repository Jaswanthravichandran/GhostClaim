import requests 
import dns.resolver

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
    "AWS S3": "The specified bucket does not exist",
    "Acquia": "Web Site Not Found",
    "Agile CRM": "Sorry, this page is no longer available.",
    "Airee.ru": "Ошибка 402. Сервис Айри.рф не оплачен",
    "Anima": "The page you were looking for does not exist.",
    "Bitbucket": "Repository not found",
    "Campaign Monitor": "Trying to access your account?",
    "Canny": "Company Not Found There is no such company. Did you enter the right URL?",
    "Cargo Collective": "404 Not Found",
    "Desk": "Please try again or try Desk.com free for 14 days.",
    "Digital Ocean": "Domain uses DO name servers with no records in DO.",
    "Dreamhost": "Site Not Found Well, this is awkward. The site you're looking for is not here.",
    "Fastly": "Fastly error: unknown domain",
    "Feedpress": "The feed has not been found.",
    "Freshdesk": "We couldn't find servicedesk.victim.tld Maybe this is still fresh! You can claim it now at http://www.freshservice.com/signup",
    "Frontify": "404 - Page Not Found Oops… looks like you got lost",
    "Gemfury": "404: This page could not be found.",
    "Getresponse": "With GetResponse Landing Pages, lead generation has never been easier",
    "Ghost": "Site unavailable.|Failed to resolve DNS path for this host",
    "Google Cloud Storage": "The specified bucket does not exist.",
    "Google Sites": "The requested URL was not found on this server. That’s all we know.",
    "HatenaBlog": "404 Blog is not found",
    "Help Juice": "We could not find what you're looking for.",
    "Help Scout": "No settings were found for this company:",
    "Helprace": "HTTP_STATUS=301",
    "HubSpot": "This page isn't available",
    "Intercom": "Uh oh. That page doesn't exist.",
    "JetBrains": "is not a registered InCloud YouTrack",
    "Kinsta": "No Site For Domain",
    "Landingi": "It looks like you’re lost...",
    "LaunchRock": "HTTP_STATUS=500",
    "Mailchimp": "We can't find that page It looks like you're trying to reach a page that was built by Mailchimp but is no longer active.",
    "Microsoft Azure": "NXDOMAIN",
    "Ngrok": "Tunnel .*.ngrok.io not found",
    "Pantheon": "404 error unknown site!",
    "Pingdom": "Sorry, couldn't find the status page",
    "Readme.io": "The creators of this project are still working on making everything perfect!",
    "Readthedocs": "The link you have followed or the URL that you entered does not exist.",
    "Short.io": "Link does not exist",
    "SmartJobBoard": "This job board website is either expired or its domain name is invalid.",
    "Strikingly": "PAGE NOT FOUND.",
    "Surge.sh": "project not found",
    "SurveySparrow": "Account not found.",
    "Tumblr": "Whatever you were looking for doesn't currently exist at this address",
    "Uberflip": "The URL you've accessed does not provide a hub.",
    "Uptimerobot": "page not found",
    "Vercel": "DEPLOYMENT_NOT_FOUND.",
    "Webflow": "The page you are looking for doesn't exist or has been moved.",
    "Wix": "Looks Like This Domain Isn't Connected To A Website Yet!",
    "Wordpress": "Do you want to register .*.wordpress.com?",
    "Worksites": "Hello! Sorry, but the website you’re looking for doesn’t exist.",
    }


    def __init__(self, subdomain_file, log_txt_file, vuln_domain):
        self.subdomain_file = subdomain_file
        self.log_txt = log_txt_file
        self.vuln_domain = vuln_domain

    def _fetch_response(self, domain):
        try:
            url = f"https://{domain}"
            r = requests.get(url, timeout=5)
            return r.status_code, r.text
        except requests.RequestException as e:
            return None, str(e)

    def _check_cname(self, domain):
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                cname_target = str(rdata.target).rstrip('.')
                return cname_target
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.exception.DNSException):
            return None

    def _detect_takeover(self, response):
        for service, fingerprint in self.FINGERPRINTS.items():
            if fingerprint in response:
                return True, service
        return False, None

    def check_subdomain_takeover(self):
        try:
            with open(self.subdomain_file, "r") as file:
                subdomains = file.readlines()
            with open(self.log_txt, "w") as log_file, open(self.vuln_domain, "w") as vuln_log:
                for sub in subdomains:
                    sub = sub.strip()
                    print(f"{self.CYAN}[~] Scanning: {sub}{self.RESET}")

                    cname_target = self._check_cname(sub)
                        
                    if cname_target:
                        print(f"{self.GREEN}    [+] CNAME → {cname_target}{self.RESET}")
                        if any(keyword in cname_target for keyword in [
                            "github.io", "herokuapp.com", "amazonaws.com", "vercel.app", "readthedocs.io"
                        ]):
                            print(f"{self.RED}    [!] CNAME points to potential vulnerable host: {cname_target}{self.RESET}")
                            log_file.write(f"{self.RED}    [!] CNAME points to potential vulnerable host: {cname_target}{self.RESET}\n")

                    status_code, response = self._fetch_response(sub)

                    if status_code:
                        vulnerable, service = self._detect_takeover(response)
                        if vulnerable:
                            print(f"{self.RED}    [!] Fingerprint matched → Potential Subdomain Takeover via {service}{self.RESET}")
                            log_file.write(f"{self.RED}    [!] Fingerprint matched → Potential Subdomain Takeover via {service}{self.RESET}\n")
                            vuln_log.write(sub + "\n")
                        elif status_code in [404, 410, 301, 503, 502]:
                            print(f"{self.YELLOW}    [!] Status Code {status_code} → Might be unclaimed (manual check recommended){self.RESET}")
                            log_file.write(f"{self.YELLOW}    [!] Status Code {status_code} → Might be unclaimed (manual check recommended){self.RESET}\n")
                            vuln_log.write(sub + "\n")
                        else:
                            print(f"{self.GREEN}    [-] {sub} looks safe (HTTP {status_code}){self.RESET}")
                            log_file.write(f"{self.GREEN}    [-] {sub} looks safe (HTTP {status_code}){self.RESET}")
                    else:
                        #print(f"{self.RED}    [x] Failed to connect to {sub} - {response}{self.RESET}")
                        log_file.write(f"{self.RED}    [x] Failed to connect to {sub} - {response}{self.RESET}")

        except FileNotFoundError:
            print(f"{self.RED}[-] Subdomain file not found: {self.subdomain_file}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}[-] Unexpected error: {e}{self.RESET}")


