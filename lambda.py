import boto3

def get_ec2_client():
    
    try:
        ec2_client = boto3.client('ec2', region_name='us-east-1')
        
    except Exception as e:
        print(e)
        
    else:
        return ec2_client
    
def get_default_vpc(ec2_client):
    
    default_vpc = ec2_client.describe_vpcs(
        Filters=[ {'Name' : 'isDefault','Values' : ['true']}, {'Name': 'state', 'Values': ['available']}]
        )
        
    if default_vpc['Vpcs']:
        return default_vpc['Vpcs'][0]['VpcId']
    
def get_ec2_instances(ec2_client, default_vpc_id):
    ec2_instances_list = []
    response = ec2_client.describe_instances(
        Filters=[ {'Name': 'instance-type', 'Values': ['m5.large']} , {'Name': 'vpc-id', 'Values': [default_vpc_id]} ]
        )
        
    for i in response['Reservations']:
        for j in i['Instances']:
            ec2_instances_list.append(j['InstanceId'])
            
    return ec2_instances_list
    

def lambda_handler(event, context):
    
    ec2_client = get_ec2_client()
    if ec2_client:
        default_vpc_id = get_default_vpc(ec2_client)
    if default_vpc_id:
        ec2_instances_list = get_ec2_instances(ec2_client, default_vpc_id)
        print(ec2_instances_list)
