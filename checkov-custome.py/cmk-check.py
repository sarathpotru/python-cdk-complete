from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3
from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3
from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import boto3




class CustomEncryptionCheck(BaseResourceCheck):
    def __init__(self):
        name = "Enforce encryption using customer KMS key"
        id = "CUSTOM_ENCRYPTION_CHECK"
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("encrypted"):
            if not conf.get("kms_key_id"):
                return CheckResult.FAILED
            else:
                # Verify if the KMS key exists and is customer-managed
                kms_key_id = conf["kms_key_id"]
                kms_client = boto3.client("kms")
                response = kms_client.describe_key(KeyId=kms_key_id)
                if response.get("KeyMetadata").get("KeyManager") != "CUSTOMER":
                    return CheckResult.FAILED
        return CheckResult.PASSED

class CustomIMDSv2Check(BaseResourceCheck):
    def __init__(self):
        name = "Ensure EC2 instances use IMDSv2"
        id = "CUSTOM_IMDSV2_CHECK"
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("metadata_options"):
            if not conf["metadata_options"].get("http_tokens") or conf["metadata_options"]["http_tokens"] != "required":
                return CheckResult.FAILED
        return CheckResult.PASSED

class CustomDefaultSecurityGroupCheck(BaseResourceCheck):
    def __init__(self):
        name = "Default security group restricts all traffic"
        id = "CUSTOM_DEFAULT_SG_CHECK"
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("name") == "default" and conf.get("ingress") and conf.get("egress"):
            # Check if ingress and egress rules exist
            ingress_rules = conf["ingress"]
            egress_rules = conf["egress"]
            if len(ingress_rules) == 0 and len(egress_rules) == 0:
                return CheckResult.FAILED
        return CheckResult.PASSED
    
class CustomKinesisEncryptionCheck(BaseResourceCheck):
    def __init__(self):
        name = "Enforce encryption using server-side encryption for Kinesis Streams"
        id = "CUSTOM_KINESIS_ENCRYPTION_CHECK"
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("server_side_encryption"):
            encryption_type = conf["server_side_encryption"][0]["encryption_type"]
            if encryption_type != "KMS" and not conf["server_side_encryption"][0].get("key_arn"):
                return CheckResult.FAILED
        return CheckResult.PASSED


class CustomELBAccessLoggingCheck(BaseResourceCheck):
    def __init__(self):
        name = "ELB access logging is enabled"
        id = "CUSTOM_ELB_ACCESS_LOGGING_CHECK"
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("access_logs"):
            if not conf["access_logs"][0].get("enabled"):
                return CheckResult.FAILED
        return CheckResult.PASSED


class CustomIAMPasswordPolicyCheck(BaseResourceCheck):
    def __init__(self):
        name = "IAM password policy has a 90-day expiration"
        id = "CUSTOM_IAM_PASSWORD_POLICY_CHECK"
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        iam_client = boto3.client("iam")
        password_policy = iam_client.get_account_password_policy()
        max_password_age = password_policy["PasswordPolicy"].get("MaxPasswordAge")
        if max_password_age is None or int(max_password_age) != 90:
            return CheckResult.FAILED
        return CheckResult.PASSED

class CustomSubnetPublicIPCheck(BaseResourceCheck):
    def __init__(self):
        name = "VPC subnets do not allow automatic public IP assignments"
        id = "CUSTOM_SUBNET_PUBLIC_IP_CHECK"
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("map_public_ip_on_launch"):
            if conf["map_public_ip_on_launch"]:
                return CheckResult.FAILED
        return CheckResult.PASSED

class CustomRDSMinorUpgradesCheck(BaseResourceCheck):
    def __init__(self):
        name = "RDS minor upgrades are disabled"
        id = "CUSTOM_RDS_MINOR_UPGRADES_CHECK"
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("auto_minor_version_upgrade"):
            if conf["auto_minor_version_upgrade"]:
                return CheckResult.FAILED
        return CheckResult.PASSED

class CustomDynamoDBEncryptionCheck(BaseResourceCheck):
    def __init__(self):
        name = "DynamoDB tables are encrypted using customer-managed CMK"
        id = "CUSTOM_DYNAMODB_ENCRYPTION_CHECK"
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories)

    def scan_resource_conf(self, conf):
        if conf.get("server_side_encryption"):
            encryption_type = conf["server_side_encryption"][0]["encryption_type"]
            if encryption_type == "AWS_OWNED_CMK":
                return CheckResult.FAILED
        return CheckResult.PASSED



from checkov.terraform.checks.provider.aws.registry import aws_registry

aws_registry.register(CustomEncryptionCheck())
aws_registry.register(CustomIMDSv2Check())

# Run Checkov scan on your Terraform files
checkov_results = Runner().run(root_folder="<path-to-terraform-root-folder>")


