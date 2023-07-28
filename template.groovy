@GrabResolver(name='aws-sdk', root='https://repo1.maven.org/maven2/')
@Grab('com.amazonaws:aws-java-sdk-cloudformation:1.12.67')

import com.amazonaws.auth.BasicAWSCredentials
import com.amazonaws.regions.Regions
import com.amazonaws.services.cloudformation.AmazonCloudFormationClientBuilder
import com.amazonaws.services.cloudformation.model.CreateStackRequest
import com.amazonaws.services.cloudformation.model.UpdateStackRequest
import com.amazonaws.services.cloudformation.model.Parameter

def accessKeyId = 'YOUR_ACCESS_KEY_ID'
def secretKey = 'YOUR_SECRET_ACCESS_KEY'
def regionName = 'us-east-1'
def existingStackName = 'ExistingStack'
def newStackName = 'NewStack'
def existingTemplateURL = 'https://s3.amazonaws.com/bucket-name/your-existing-template.yml'
def newTemplateURL = 'https://s3.amazonaws.com/bucket-name/your-new-template.yml'

def awsCredentials = new BasicAWSCredentials(accessKeyId, secretKey)
def cfnClient = AmazonCloudFormationClientBuilder.standard()
        .withRegion(Regions.fromName(regionName))
        .withCredentials(awsCredentials)
        .build()

// Run the existing CloudFormation stack
def existingStackRequest = new CreateStackRequest()
existingStackRequest.setStackName(existingStackName)
existingStackRequest.setTemplateURL(existingTemplateURL)
def existingStackResponse = cfnClient.createStack(existingStackRequest)

// Wait for the stack creation to complete
cfnClient.waitForStackCreateComplete(existingStackName)

// Deploy the new CloudFormation stack
def newStackRequest = new UpdateStackRequest()
newStackRequest.setStackName(newStackName)
newStackRequest.setTemplateURL(newTemplateURL)
newStackRequest.setCapabilities(['CAPABILITY_IAM']) // If your template requires IAM capabilities
newStackRequest.setParameters([
        new Parameter().withParameterKey('ParameterName1').withParameterValue('ParameterValue1'),
        new Parameter().withParameterKey('ParameterName2').withParameterValue('ParameterValue2'),
        // Add more parameters as needed
])
def newStackResponse = cfnClient.updateStack(newStackRequest)

// Wait for the stack update to complete
cfnClient.waitForStackUpdateComplete(newStackName)
