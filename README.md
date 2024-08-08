# Misc

Collection of scripts to help with AWS dangling DNS records.

## Features

- Fetches current AWS IP ranges
- Performs DNS lookups on subdomains
- Identifies if resolved IPs are within AWS ranges
- Provides AWS region information for matching IPs
- Tries to brute-force allocate elastic IP on target IP.

## Requirements

- Python 3.6+
- `requests` library
- `dnspython` library
- `boto3`library

## Installation

1. Clone this repository or download the script.
2. Install the required libraries:
   ```
   pip3 install requests dnspython boto3
   ```

## Usage

1. Create a text file with subdomains (one per line):
   ```
   example.com
   subdomain.example.com
   ```

2. Run the IP check script:
   ```
   python3 aws_ip_check.py subdomains.txt
   ```

## Output

The script will output information for subdomains resolving to AWS IP addresses:

```
Subdomain: example.com, IP: 192.0.2.1, CIDR: 192.0.2.0/24, Region: us-east-1
```

## Note

This script requires an active internet connection to fetch AWS IP ranges and perform DNS lookups.

