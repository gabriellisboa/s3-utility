import sys
import boto3
from model.S3_bucket import S3_bucket

client = boto3.client('s3')

bucket_list = client.list_buckets()

for bucket in bucket_list['Buckets']:
    s3_bucket = S3_bucket(bucket['Name'], bucket['CreationDate'])
    if sys.argv.count('--extra-info') > 0:
        s3_bucket.print_all_info()
    else:
        s3_bucket.print_basic_info()
    print('------------------------------------')
