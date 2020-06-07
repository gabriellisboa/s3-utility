import boto3

class Regions_service():
    def __init__(self):
        self.regions = self.get_aws_regions()

    def get_aws_regions(self):
        ssm_client = boto3.client('ssm')
        raw_regions = ssm_client.get_parameters_by_path(Path='/aws/service/global-infrastructure/regions')

        # TODO: check if this is all regions
        all_region_short_names = [short_name["Value"] for short_name in raw_regions["Parameters"]]
        all_region_names = []

        for short_name in all_region_short_names:
            region_name = ssm_client.get_parameter(Name=f'/aws/service/global-infrastructure/regions/{short_name}/longName')
            all_region_names.append({short_name: region_name["Parameter"]["Value"]})
        return all_region_names