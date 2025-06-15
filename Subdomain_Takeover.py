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


