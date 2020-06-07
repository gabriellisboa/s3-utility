import boto3
import json
from datetime import datetime, timedelta
from service.aws.regions import Regions_service

class S3_service():
    def __init__(self):
        self.start_date = datetime.now() - timedelta(days=15)
        self.end_time = datetime.now()
    
    def get_total_objects_by_name (self, name):
        cloudwatch = boto3.client('cloudwatch')

        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName='NumberOfObjects',
            Dimensions=[
                {
                    'Name': 'BucketName',
                    'Value': name
                },
                {
                    'Name': 'StorageType',
                    'Value': 'AllStorageTypes'
                }
            ],
            StartTime=self.start_date,
            EndTime=self.end_time,
            Period=2592000,
            Statistics=['Average']
        )
        if response['Datapoints'] != []:
            return response['Datapoints'][0]['Average']
        else:
            return 0

    def get_sizes_by_name(self, name):
        cloudwatch = boto3.client('cloudwatch')
        all_storage_types = [
            'StandardStorage',
            'StandardIAStorage',
            'OneZoneIAStorage',
            'DeepArchiveStorage',
        ]

        size_list = []

        for storage_type in all_storage_types:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {
                        'Name': 'BucketName',
                        'Value': name
                    },
                    {
                        'Name': 'StorageType',
                        'Value': storage_type
                    }
                ],
                StartTime=self.start_date,
                EndTime=self.end_time,
                Period=2592000,
                Statistics=['Average']
            )
            if response['Datapoints'] != []:
                size_list.append({'type': storage_type, 'value': response['Datapoints'][0]['Average']})
        return size_list

    def get_sorted_objects_by_bucket_name (self, name, reverse=False):
        client = boto3.client('s3')
        lambda_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        raw_objs = client.list_objects_v2(Bucket=name)
        if 'Contents' in raw_objs:
            objs = raw_objs['Contents']
            return [obj for obj in sorted(objs, key=lambda_last_modified, reverse=reverse)]
        else:
            return []

    def get_storage_prices_for_region(self, region):
        client = boto3.client('pricing')
        aws_regions = Regions_service()
        formated_region = 'US East (N. Virginia)'

        if region != 'us-east-1':
            for region_value in aws_regions.regions:
                if region in region_value:
                    formated_region = region_value[region]

        all_products = client.get_products(
            ServiceCode='AmazonS3',
            Filters=[
            {
                'Field': 'location',
                'Type': 'TERM_MATCH',
                'Value': formated_region,
            }
            ],
            FormatVersion='aws_v1',
            MaxResults=100,
        )

        product_price_list = []

        for product_string in all_products['PriceList']:
            product = json.loads(product_string)
            if 'productFamily' in product['product']:
                if product['product']['productFamily'] == 'Storage':
                    formated_product = {}
                    formated_product['sku'] = product['product']['sku']
                    formated_product['volumeType'] = product['product']['attributes']['volumeType']
                    formated_product['storageClass'] = product['product']['attributes']['storageClass']
                    price_dimension = next(value['priceDimensions'] for key,value in product['terms']['OnDemand'].items() if formated_product['sku'] in key)
                    formated_product['pricePerUnit'] = next(value['pricePerUnit'] for key,value in price_dimension.items() if formated_product['sku'] in key)
                    product_price_list.append(formated_product)
        return product_price_list

    def get_bucket_location_by_name(self, name):
        client = boto3.client('s3')
        response = client.get_bucket_location(Bucket=name)

        if response['LocationConstraint'] == None:
            return 'us-east-1'
        else:
            return response['LocationConstraint']
