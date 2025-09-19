import dns.resolver

domain = "dev.vc.logitech.com"

def resolve_dns_records(domain):
    types = ['CNAME', 'A', 'AAAA']
    for rtype in types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                print(f"{rtype} record: {rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"[!] No {rtype} record found for {domain}")
        except dns.resolver.NXDOMAIN:
            print(f"[!] Domain {domain} does not exist")
            break
        except dns.exception.Timeout:
            print(f"[!] Timeout querying {rtype} for {domain}")
        except Exception as e:
            print(f"[!] Error querying {rtype} for {domain}: {e}")

resolve_dns_records(domain)
