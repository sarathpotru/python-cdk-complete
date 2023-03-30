from aws_cdk import core
from aws_cdk import aws_cloudhsmv2 as cloudhsm

class CloudHSMStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the CloudHSM cluster
        hsm_cluster = cloudhsm.CfnCluster(
            self, "HSMCluster",
            subnet_ids=["subnet-123456", "subnet-789012"],
            hsm_type="hsm1.medium",
            source_backup_id="backup-123456",
            tags=[core.CfnTag(key="Name", value="MyHSMCluster")],
        )

        # Create the CloudHSM client
        hsm_client = cloudhsm.CfnClient(
            self, "HSMClient",
            cluster_id=hsm_cluster.ref,
            subnet_ids=["subnet-123456"],
            tags=[core.CfnTag(key="Name", value="MyHSMClient")],
        )

app = core.App()
CloudHSMStack(app, "CloudHSMStack")
app.synth()