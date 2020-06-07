import re
from service.aws.s3 import S3_service
from utils.bytes_to import bytesto

class S3_bucket():
    def __init__(self, name, creation_date):
        s3_service = S3_service()

        self.name = name
        self.creation_date = creation_date
        self.region = s3_service.get_bucket_location_by_name(name)
        self.objects_count = s3_service.get_total_objects_by_name(name)
        self.sizes = s3_service.get_sizes_by_name(name)
        self.objects = s3_service.get_sorted_objects_by_bucket_name(name, True)
        self.last_modified = self.get_last_modified()
        self.storage_info = self.get_storage_info(self.sizes)
        self.total_price = self.get_total_price(self.storage_info)
        self.total_size = self.get_total_size(self.storage_info)

    def get_last_modified(self):
        if not self.objects:
            return self.creation_date
        else:
            return self.objects[0]['LastModified']

    def create_storage_price(self, size, price):
        return {
            'type': size['type'],
            'GbSize': bytesto(size['value'], 'g'),
            'total_price': bytesto(size['value'], 'g') * float(price['pricePerUnit']['USD'])
        }

    def get_storage_info(self, sizes):
        s3_service = S3_service()
        size_list = sizes
        storage_prices = s3_service.get_storage_prices_for_region(self.region)

        price_per_storage = []

        for size in size_list:
            words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', size['type'])
            for price in storage_prices:
                if words[0] == price['volumeType'] and  words[1] != 'IA':
                    price_per_storage.append(self.create_storage_price(size, price))

                elif words[0] == price['volumeType'] and  words[1] == 'IA':
                    price_per_storage.append(self.create_storage_price(size, price))

                elif price['volumeType'].startswith(f'{words[0]} {words[1]}'):
                    price_per_storage.append(self.create_storage_price(size, price))

                elif price['volumeType'].startswith('Amazon Glacier') and words[0] == 'Deep':
                    price_per_storage.append(self.create_storage_price(size, price))
        return price_per_storage

    def get_total_price(self, storage_info):
        total = 0
        for storage in storage_info:
            total+= storage['total_price']
        return total

    def get_total_size(self, storage_info):
        total = 0
        for storage in storage_info:
            total+= storage['GbSize']
        return total




    def print_basic_info (self):
        print(f'name: {self.name}')
        print(f'creation_date: {self.creation_date}')
        print(f'objects_count: {self.objects_count:.2f}')
        print(f'total_size: {self.total_size:.2f} GB')
        print(f'last_modified: {self.last_modified}')
        print(f'total_price: USD {self.total_price:.2f}')

    
    def print_all_info (self):
        print(f'name: {self.name}')
        print(f'creation_date: {self.creation_date}')
        print(f'region: {self.region}')
        print(f'objects_count: {self.objects_count:.2f}')
        print(f'total_size: {self.total_size:.2f} GB')
        print(f'last_modified: {self.last_modified}')
        print(f'total_price: {self.total_price:.2f}')