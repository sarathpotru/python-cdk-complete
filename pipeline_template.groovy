pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the Terraform repository
                git 'https://github.com/your-terraform-repo.git'
            }
        }

        stage('Deploy - Dev') {
            steps {
                // Change to the dev workspace
                sh 'cd /path/to/terraform/repo'
                sh 'terraform workspace select dev'

                // Deploy the dev environment
                sh 'terraform init -backend-config=backend-dev.tfvars'
                sh 'terraform apply -var-file=dev.tfvars -auto-approve'
            }
        }

        stage('Deploy - QA') {
            steps {
                // Change to the qa workspace
                sh 'cd /path/to/terraform/repo'
                sh 'terraform workspace select qa'

                // Deploy the qa environment
                sh 'terraform init -backend-config=backend-qa.tfvars'
                sh 'terraform apply -var-file=qa.tfvars -auto-approve'
            }
        }

        stage('Deploy - Prod') {
            steps {
                // Change to the prod workspace
                sh 'cd /path/to/terraform/repo'
                sh 'terraform workspace select prod'

                // Deploy the prod environment
                sh 'terraform init -backend-config=backend-prod.tfvars'
                sh 'terraform apply -var-file=prod.tfvars -auto-approve'
            }
        }

        stage('Cleanup') {
            steps {
                // Change to the prod workspace
                sh 'cd /path/to/terraform/repo'
                sh 'terraform workspace select prod'

                // Destroy the prod environment
                sh 'terraform init -backend-config=backend-prod.tfvars'
                sh 'terraform destroy -var-file=prod.tfvars -auto-approve'
            }
        }
    }

    post {
        always {
            // Clean up any remaining artifacts
            deleteDir()
        }
    }
}
