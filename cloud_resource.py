#!/usr/bin/env python3
# encoding: utf-8

import boto3
import warnings

def ec2_list():
    print("EC2 list")
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions')
    # regions = [{'Endpoint': 'ec2.us-west-1.amazonaws.com', 'RegionName': 'us-west-1', 'OptInStatus': 'opt-in-not-required'}]

    total_ec2 = 0
    for region in regions:
        split_line("-")
        print(region.get("RegionName"))
        session = boto3.Session(
            region_name=region.get("RegionName"),
            profile_name='pc'
        )
        ec2_client = session.client('ec2')
        dict_of_ec2 = ec2_client.describe_instances().get("Reservations")
        ec2list = []
        for reservation in dict_of_ec2:
            for instance in reservation['Instances']:
                ec2instance = instance.get("InstanceId")
                ec2list.append(ec2instance)
                total_ec2 += 1

        i = 0
        while i < len(ec2list):
            ec2_instance_name = ec2list[i]
            try:
                response = ec2_client.describe_tags(Filters=[
                    {
                        'Name': 'resource-id',
                        'Values': [ec2_instance_name],
                    },
                ],)
                tags = response['Tags']
                if have_tag(tags,'Owner') and have_tag(tags,'Project'):
                    print(ec2_instance_name+' has proper tags')
                else:
                    print(ec2_instance_name+' doesn\'t have proper tags', end=" ")
                    print(tags)
            except ClientError:
                print(ec2_instance_name, "error")
            i += 1
    print("Total ec2: ", end="")
    print(total_ec2)

def split_line(splitter):
    print(splitter*40)

def have_tag(dictionary: dict, tag_key: str):
    """Search tag key
    """
    tags = (tag_key.capitalize(), tag_key.lower())
    if dictionary is not None:
        dict_with_owner_key = [tag for tag in dictionary if tag["Key"] in tags]
        if dict_with_owner_key:
            return dict_with_owner_key[0]['Value']
    return None

def rds_list():
    print("RDS list")
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions')
    # regions = [{'Endpoint': 'ec2.us-west-1.amazonaws.com', 'RegionName': 'us-west-1', 'OptInStatus': 'opt-in-not-required'}]
    # print(regions)

    total_rds = 0
    
    for region in regions:
        split_line("-")
        print(region.get("RegionName"))
        session = boto3.Session(
            region_name=region.get("RegionName"),
            profile_name='pc'
        )
        rds_client = session.client('rds')
        dict_of_rds = rds_client.describe_db_instances().get("DBInstances")
        # print(dict_of_rds)
        if dict_of_rds:
            for i in dict_of_rds:
                total_rds += 1
                arn = i['DBInstanceArn']
                # arn:aws:rds:ap-southeast-1::db:mydb
                tags = rds_client.list_tags_for_resource(ResourceName=arn)['TagList']
                # print(arn+" owner is ")
                if have_tag(tags,'Owner') and have_tag(tags,'Project'):
                    print(arn+' has proper tags')
                else:
                    print(arn+' doesn\'t have proper tags', end=" ")
                    print(tags)
                # print(tags)
    print("Total rds: ", end="")
    print(total_rds)
        

# https://github.com/boto/botocore/issues/2705
warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')
ec2_list()
split_line("=")
rds_list()
