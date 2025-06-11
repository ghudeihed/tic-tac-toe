#!/bin/bash

# AWS Infrastructure Setup Script for Tic-Tac-Toe Application
# This script sets up the basic AWS infrastructure needed for deployment

set -e  # Exit on any error

# Configuration variables
AWS_REGION="${AWS_REGION:-us-east-1}"
APP_NAME="tic-tac-toe"
CLUSTER_NAME="${APP_NAME}-cluster"
SERVICE_NAME="${APP_NAME}-service"
LOG_GROUP_NAME="/ecs/${APP_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if AWS CLI is installed and configured
check_aws_cli() {
    log_info "Checking AWS CLI configuration..."
    
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        log_info "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS CLI is not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log_success "AWS CLI configured for account: $AWS_ACCOUNT_ID"
}

# Create ECS cluster
create_ecs_cluster() {
    log_info "Creating ECS cluster: $CLUSTER_NAME"
    
    if aws ecs describe-clusters --clusters $CLUSTER_NAME --region $AWS_REGION &> /dev/null; then
        log_warning "ECS cluster $CLUSTER_NAME already exists"
    else
        aws ecs create-cluster \
            --cluster-name $CLUSTER_NAME \
            --capacity-providers FARGATE \
            --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
            --region $AWS_REGION
        log_success "Created ECS cluster: $CLUSTER_NAME"
    fi
}

# Create ECR repositories
create_ecr_repositories() {
    log_info "Creating ECR repositories..."
    
    for repo in "${APP_NAME}-backend" "${APP_NAME}-frontend"; do
        if aws ecr describe-repositories --repository-names $repo --region $AWS_REGION &> /dev/null; then
            log_warning "ECR repository $repo already exists"
        else
            aws ecr create-repository \
                --repository-name $repo \
                --image-scanning-configuration scanOnPush=true \
                --region $AWS_REGION
            log_success "Created ECR repository: $repo"
        fi
        
        # Set lifecycle policy to manage image retention
        aws ecr put-lifecycle-policy \
            --repository-name $repo \
            --lifecycle-policy-text '{
                "rules": [
                    {
                        "rulePriority": 1,
                        "description": "Keep last 10 images",
                        "selection": {
                            "tagStatus": "any",
                            "countType": "imageCountMoreThan",
                            "countNumber": 10
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }' \
            --region $AWS_REGION
    done
}

# Create CloudWatch log group
create_log_group() {
    log_info "Creating CloudWatch log group: $LOG_GROUP_NAME"
    
    if aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP_NAME --region $AWS_REGION | grep -q $LOG_GROUP_NAME; then
        log_warning "Log group $LOG_GROUP_NAME already exists"
    else
        aws logs create-log-group \
            --log-group-name $LOG_GROUP_NAME \
            --region $AWS_REGION
        
        # Set retention policy (30 days)
        aws logs put-retention-policy \
            --log-group-name $LOG_GROUP_NAME \
            --retention-in-days 30 \
            --region $AWS_REGION
        
        log_success "Created CloudWatch log group: $LOG_GROUP_NAME"
    fi
}

# Create IAM roles
create_iam_roles() {
    log_info "Creating IAM roles..."
    
    # ECS Task Execution Role
    EXECUTION_ROLE_NAME="ecsTaskExecutionRole"
    if aws iam get-role --role-name $EXECUTION_ROLE_NAME &> /dev/null; then
        log_warning "IAM role $EXECUTION_ROLE_NAME already exists"
    else
        # Create trust policy
        cat > /tmp/ecs-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
        
        aws iam create-role \
            --role-name $EXECUTION_ROLE_NAME \
            --assume-role-policy-document file:///tmp/ecs-trust-policy.json
        
        aws iam attach-role-policy \
            --role-name $EXECUTION_ROLE_NAME \
            --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
        
        # Add permissions for Secrets Manager
        aws iam attach-role-policy \
            --role-name $EXECUTION_ROLE_NAME \
            --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
        
        log_success "Created IAM role: $EXECUTION_ROLE_NAME"
        rm /tmp/ecs-trust-policy.json
    fi
    
    # ECS Task Role (for application permissions)
    TASK_ROLE_NAME="ecsTaskRole"
    if aws iam get-role --role-name $TASK_ROLE_NAME &> /dev/null; then
        log_warning "IAM role $TASK_ROLE_NAME already exists"
    else
        aws iam create-role \
            --role-name $TASK_ROLE_NAME \
            --assume-role-policy-document file:///tmp/ecs-trust-policy.json
        
        log_success "Created IAM role: $TASK_ROLE_NAME"
    fi
}

# Create Secrets Manager secrets
create_secrets() {
    log_info "Creating Secrets Manager secrets..."
    
    # Create SECRET_KEY
    SECRET_NAME="${APP_NAME}/SECRET_KEY"
    if aws secretsmanager describe-secret --secret-id $SECRET_NAME --region $AWS_REGION &> /dev/null; then
        log_warning "Secret $SECRET_NAME already exists"
    else
        # Generate a random secret key
        SECRET_VALUE=$(openssl rand -base64 32)
        aws secretsmanager create-secret \
            --name $SECRET_NAME \
            --description "Flask secret key for ${APP_NAME}" \
            --secret-string $SECRET_VALUE \
            --region $AWS_REGION
        log_success "Created secret: $SECRET_NAME"
    fi
    
    # Create SENTRY_DSN placeholder
    SENTRY_SECRET_NAME="${APP_NAME}/SENTRY_DSN"
    if aws secretsmanager describe-secret --secret-id $SENTRY_SECRET_NAME --region $AWS_REGION &> /dev/null; then
        log_warning "Secret $SENTRY_SECRET_NAME already exists"
    else
        aws secretsmanager create-secret \
            --name $SENTRY_SECRET_NAME \
            --description "Sentry DSN for ${APP_NAME}" \
            --secret-string "https://your-sentry-dsn@sentry.io/project-id" \
            --region $AWS_REGION
        log_success "Created secret: $SENTRY_SECRET_NAME (update with real Sentry DSN)"
    fi
}

# Update task definition with actual values
update_task_definition() {
    log_info "Updating task definition with actual AWS account ID..."
    
    if [ -f ".aws/task-definition.json" ]; then
        # Create backup
        cp .aws/task-definition.json .aws/task-definition.json.backup
        
        # Replace placeholders
        sed -i.tmp "s/YOUR_ACCOUNT_ID/$AWS_ACCOUNT_ID/g" .aws/task-definition.json
        rm .aws/task-definition.json.tmp
        
        log_success "Updated task definition with account ID: $AWS_ACCOUNT_ID"
    else
        log_warning "Task definition file not found at .aws/task-definition.json"
    fi
}

# Print next steps
print_next_steps() {
    log_success "AWS infrastructure setup complete!"
    echo
    log_info "📋 Next Steps:"
    echo "1. 🔐 Set up GitHub Secrets in your repository:"
    echo "   - AWS_ACCESS_KEY_ID"
    echo "   - AWS_SECRET_ACCESS_KEY"
    echo
    echo "2. 🔧 Update Sentry DSN secret (optional):"
    echo "   aws secretsmanager update-secret --secret-id ${APP_NAME}/SENTRY_DSN --secret-string 'your-real-sentry-dsn' --region $AWS_REGION"
    echo
    echo "3. 🌐 Set up VPC and subnets for ECS (if not using default VPC):"
    echo "   - Create VPC with public subnets"
    echo "   - Set up Internet Gateway"
    echo "   - Configure security groups"
    echo
    echo "4. ⚖️ Create Application Load Balancer:"
    echo "   - Set up ALB with target groups"
    echo "   - Configure health checks"
    echo "   - Set up SSL certificate (optional)"
    echo
    echo "5. 🚀 Create ECS Service:"
    echo "   aws ecs create-service --cluster $CLUSTER_NAME --service-name $SERVICE_NAME --task-definition tic-tac-toe --desired-count 1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}'"
    echo
    echo "6. 🔄 Push your code to trigger GitHub Actions deployment:"
    echo "   git push origin main"
    echo
    log_info "📊 Resource Summary:"
    echo "   - ECS Cluster: $CLUSTER_NAME"
    echo "   - ECR Repositories: ${APP_NAME}-backend, ${APP_NAME}-frontend"
    echo "   - CloudWatch Log Group: $LOG_GROUP_NAME"
    echo "   - IAM Roles: ecsTaskExecutionRole, ecsTaskRole"
    echo "   - Secrets: ${APP_NAME}/SECRET_KEY, ${APP_NAME}/SENTRY_DSN"
    echo "   - AWS Account: $AWS_ACCOUNT_ID"
    echo "   - Region: $AWS_REGION"
}

# Main execution
main() {
    log_info "🚀 Starting AWS infrastructure setup for $APP_NAME..."
    echo
    
    check_aws_cli
    create_ecs_cluster
    create_ecr_repositories
    create_log_group
    create_iam_roles
    create_secrets
    update_task_definition
    
    echo
    print_next_steps
}

# Run the script
main "$@"