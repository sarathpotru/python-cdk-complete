import boto3

def lambda_handler(event, context):

    client = boto3.client('cloudhsmv2')

    response = client.create_cluster(
        HsmType='hsm1.medium',
        BackupRetentionPolicy={
        'Type': 'DAYS',
        'Value': '7'
        },
        SubnetIds=[
        'subnet-0211a648cd5b639b2',
        'subnet-0388ccfadab0b09fe'
        ],
        TagList=[
            {
                'Key': 'Name',
                'Value': 'MyCluster'
            }
        ]
    )

    print(response)
    
    return {
        'statusCode': 200,
        'body': 'Cluster created successfully'
    }
