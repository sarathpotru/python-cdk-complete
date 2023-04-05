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

# get cluster ID
cluster_id = response['Cluster']['ClusterId']

response = client.create_hsm(
    ClusterId=cluster_id,
    AvailabilityZone='us-east-1b'
)
# # get HSM IDs
# response = client.describe_clusters(
#     Filters=
#         {
            
#             'clusterIds': [
#                 cluster_id,
#             ]
#         },
# )
# hsm_ids = [hsm['HsmId'] for hsm in response['Clusters'][0]['Hsms']]

# # wait for HSMs to be ready
# waiter = client.get_waiter('hsm_did_become_active')
# waiter.wait(
#     HsmIds=hsm_ids,
#     WaiterConfig={
#         'Delay': 30,
#         'MaxAttempts': 120
#     }
# )

print('HSMs are ready')
