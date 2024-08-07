import sys
import json
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import requests
import dns.resolver

def fetch_aws_ranges():
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {ipaddress.ip_network(prefix['ip_prefix']): prefix['region'] 
            for prefix in data['prefixes']}

def check_ip(ip, aws_ranges):
    ip_obj = ipaddress.ip_address(ip)
    for network, region in aws_ranges.items():
        if ip_obj in network:
            return network, region
    return None, None

def process_subdomain(subdomain, aws_ranges):
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        results = []
        for rdata in answers:
            ip = rdata.to_text()
            network, region = check_ip(ip, aws_ranges)
            if network:
                results.append((subdomain, ip, str(network), region))
        return results
    except dns.exception.DNSException:
        print(f"DNS lookup failed for {subdomain}")
        return []

def main(subdomain_file):
    print("Fetching AWS IP ranges...")
    aws_ranges = fetch_aws_ranges()
    
    with open(subdomain_file, 'r') as f:
        subdomains = [line.strip() for line in f if line.strip()]
    
    print(f"Processing {len(subdomains)} subdomains...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        all_results = executor.map(lambda s: process_subdomain(s, aws_ranges), subdomains)
    
    for results in all_results:
        for subdomain, ip, cidr, region in results:
            print(f"Subdomain: {subdomain}, IP: {ip}, CIDR: {cidr}, Region: {region}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 aws_ip_check.py <subdomain_file>")
        sys.exit(1)
    
    main(sys.argv[1])
