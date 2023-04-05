# import boto3

# def lambda_handler(event, context):

#     client = boto3.client('cloudhsmv2')

#     response = client.create_cluster(
#         HsmType='hsm1.medium',
#         BackupRetentionPolicy={
#         'Type': 'DAYS',
#         'Value': '7'
#         },
#         SubnetIds=[
#         'subnet-0211a648cd5b639b2',
#         'subnet-0388ccfadab0b09fe'
#         ],
#         TagList=[
#             {
#                 'Key': 'Name',
#                 'Value': 'MyCluster'
#             }
#         ]
#     )

#     print(response)
    
#     return {
#         'statusCode': 200,
#         'body': 'Cluster created successfully'
#     }

import boto3

client = boto3.client('cloudhsmv2')

# create HSM cluster
response = client.create_cluster(
    HsmType='hsm1.medium', # or 'hsm1.large'
    SubnetIds=['subnet-0211a648cd5b639b2'], # list of subnet IDs
    BackupRetentionPolicy={
         'Type': 'DAYS',
         'Value': '7'
         }
)
# get HSM IDs

responseid = client.describe_clusters()

hsm_ids = [hsm['HsmId'] for hsm in responseid['Clusters'][0]['Hsms']]
# get cluster ID
cluster_id = response['Cluster']['ClusterId']

# wait for HSMs to be ready
def is_hsm_activated(hsm_ids):
    response = client.describe_clusters(
        HsmIds=hsm_ids
    )
    for hsm in response['HsmList']:
        if hsm['State'] != 'ACTIVE':
            return False
    return True

# wait for HSMs to be ready
while not is_hsm_activated(hsm_ids):
    time.sleep(30)

print('The CloudHSM cluster is created: ' + cluster_id)
