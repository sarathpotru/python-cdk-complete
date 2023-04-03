import * as cdk from '@aws-cdk/core';
import * as cloudhsm from '@aws-cdk/aws-cloudhsm';

class CloudHSMStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the CloudHSM cluster
        hsm_cluster = cloudhsm.CfnCluster(
            self, "HSMCluster",
            subnet_ids=["subnet-0077f949769d577ef", "subnet-0211a648cd5b639b2"],
            hsm_type="hsm1.medium",
            tags=[core.CfnTag(key="Name", value="MyHSMCluster")],
        )

        # Create the CloudHSM client
        hsm_client = cloudhsm.CfnClient(
            self, "HSMClient",
            cluster_id=hsm_cluster.ref,
            subnet_ids=["subnet-0388ccfadab0b09fe"],
            tags=[core.CfnTag(key="Name", value="MyHSMClient")],
        )

app = core.App()
CloudHSMStack(app, "CloudHSMStack")
app.synth()