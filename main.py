from SubEnum import SubdomainEnumerator

if __name__ == "__main__":
    domain = "logitech.com"
    wordlist = "list.txt"

    enum = SubdomainEnumerator(domain, wordlist, threads=30)
    enum.enumerate()
    enum.save_to_file()

    