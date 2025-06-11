#!/bin/bash

# AWS Infrastructure Validation Script
# Validates all resources for tic-tac-toe application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID="325598860465"
APP_NAME="tic-tac-toe"

echo -e "${BLUE}🔍 AWS Infrastructure Validation for ${APP_NAME}${NC}"
echo -e "${BLUE}===============================================${NC}"
echo

# Helper functions
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check AWS CLI configuration
echo -e "${BLUE}1. AWS CLI Configuration${NC}"
echo "==============================="
if aws sts get-caller-identity &> /dev/null; then
    CURRENT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
    CURRENT_USER=$(aws sts get-caller-identity --query Arn --output text)
    log_success "AWS CLI configured"
    log_info "Account ID: $CURRENT_ACCOUNT"
    log_info "User: $CURRENT_USER"
    log_info "Region: $(aws configure get region)"
    
    if [ "$CURRENT_ACCOUNT" != "$AWS_ACCOUNT_ID" ]; then
        log_warning "Account ID mismatch! Expected: $AWS_ACCOUNT_ID, Got: $CURRENT_ACCOUNT"
    fi
else
    log_error "AWS CLI not configured or no access"
    exit 1
fi
echo

# Check ECS Cluster
echo -e "${BLUE}2. ECS Cluster${NC}"
echo "==================="
if aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION &> /dev/null; then
    CLUSTER_STATUS=$(aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION --query 'clusters[0].status' --output text)
    if [ "$CLUSTER_STATUS" = "ACTIVE" ]; then
        log_success "ECS Cluster: ${APP_NAME}-cluster (Status: $CLUSTER_STATUS)"
        
        # Get cluster details
        CAPACITY_PROVIDERS=$(aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION --query 'clusters[0].capacityProviders' --output text)
        log_info "Capacity Providers: $CAPACITY_PROVIDERS"
        
        ACTIVE_SERVICES=$(aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION --query 'clusters[0].activeServicesCount' --output text)
        RUNNING_TASKS=$(aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION --query 'clusters[0].runningTasksCount' --output text)
        log_info "Active Services: $ACTIVE_SERVICES, Running Tasks: $RUNNING_TASKS"
    else
        log_error "ECS Cluster exists but status is: $CLUSTER_STATUS"
    fi
else
    log_error "ECS Cluster ${APP_NAME}-cluster not found"
fi
echo

# Check ECR Repositories
echo -e "${BLUE}3. ECR Repositories${NC}"
echo "======================"
for repo in "backend" "frontend"; do
    if aws ecr describe-repositories --repository-names ${APP_NAME}-${repo} --region $AWS_REGION &> /dev/null; then
        REPO_URI=$(aws ecr describe-repositories --repository-names ${APP_NAME}-${repo} --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text)
        CREATED_DATE=$(aws ecr describe-repositories --repository-names ${APP_NAME}-${repo} --region $AWS_REGION --query 'repositories[0].createdAt' --output text)
        log_success "ECR Repository: ${APP_NAME}-${repo}"
        log_info "URI: $REPO_URI"
        log_info "Created: $CREATED_DATE"
        
        # Check if images exist
        IMAGE_COUNT=$(aws ecr describe-images --repository-name ${APP_NAME}-${repo} --region $AWS_REGION --query 'length(imageDetails)' --output text 2>/dev/null || echo "0")
        if [ "$IMAGE_COUNT" -gt 0 ]; then
            log_info "Images in repository: $IMAGE_COUNT"
        else
            log_warning "No images in repository yet"
        fi
    else
        log_error "ECR Repository ${APP_NAME}-${repo} not found"
    fi
done
echo

# Check CloudWatch Log Group
echo -e "${BLUE}4. CloudWatch Log Group${NC}"
echo "========================="
if aws logs describe-log-groups --log-group-name-prefix /ecs/${APP_NAME} --region $AWS_REGION | grep -q ${APP_NAME}; then
    LOG_GROUP_NAME=$(aws logs describe-log-groups --log-group-name-prefix /ecs/${APP_NAME} --region $AWS_REGION --query 'logGroups[0].logGroupName' --output text)
    RETENTION_DAYS=$(aws logs describe-log-groups --log-group-name-prefix /ecs/${APP_NAME} --region $AWS_REGION --query 'logGroups[0].retentionInDays' --output text)
    CREATION_TIME=$(aws logs describe-log-groups --log-group-name-prefix /ecs/${APP_NAME} --region $AWS_REGION --query 'logGroups[0].creationTime' --output text)
    
    log_success "CloudWatch Log Group: $LOG_GROUP_NAME"
    log_info "Retention: $RETENTION_DAYS days"
    log_info "Created: $(date -d @$(echo $CREATION_TIME/1000 | bc) 2>/dev/null || echo 'Unknown')"
else
    log_error "CloudWatch Log Group /ecs/${APP_NAME} not found"
fi
echo

# Check IAM Roles
echo -e "${BLUE}5. IAM Roles${NC}"
echo "==============="
for role in "ecsTaskExecutionRole" "ecsTaskRole"; do
    if aws iam get-role --role-name $role &> /dev/null; then
        ROLE_ARN=$(aws iam get-role --role-name $role --query 'Role.Arn' --output text)
        CREATED_DATE=$(aws iam get-role --role-name $role --query 'Role.CreateDate' --output text)
        log_success "IAM Role: $role"
        log_info "ARN: $ROLE_ARN"
        log_info "Created: $CREATED_DATE"
        
        # Check attached policies
        POLICIES=$(aws iam list-attached-role-policies --role-name $role --query 'AttachedPolicies[].PolicyName' --output text)
        if [ ! -z "$POLICIES" ]; then
            log_info "Attached Policies: $POLICIES"
        fi
    else
        log_error "IAM Role $role not found"
    fi
done
echo

# Check Secrets Manager
echo -e "${BLUE}6. Secrets Manager${NC}"
echo "===================="
for secret in "SECRET_KEY" "SENTRY_DSN"; do
    SECRET_NAME="${APP_NAME}/${secret}"
    if aws secretsmanager describe-secret --secret-id $SECRET_NAME --region $AWS_REGION &> /dev/null; then
        SECRET_ARN=$(aws secretsmanager describe-secret --secret-id $SECRET_NAME --region $AWS_REGION --query 'ARN' --output text)
        CREATED_DATE=$(aws secretsmanager describe-secret --secret-id $SECRET_NAME --region $AWS_REGION --query 'CreatedDate' --output text)
        log_success "Secret: $SECRET_NAME"
        log_info "ARN: $SECRET_ARN"
        log_info "Created: $CREATED_DATE"
    else
        log_error "Secret $SECRET_NAME not found"
    fi
done
echo

# Check Task Definition File
echo -e "${BLUE}7. Task Definition File${NC}"
echo "========================="
TASK_DEF_FILE=".aws/task-definition.json"
if [ -f "$TASK_DEF_FILE" ]; then
    log_success "Task definition file exists: $TASK_DEF_FILE"
    
    # Validate JSON
    if jq empty "$TASK_DEF_FILE" 2>/dev/null; then
        log_success "Task definition file is valid JSON"
        
        FAMILY=$(jq -r '.family' "$TASK_DEF_FILE")
        CPU=$(jq -r '.cpu' "$TASK_DEF_FILE")
        MEMORY=$(jq -r '.memory' "$TASK_DEF_FILE")
        CONTAINERS=$(jq -r '.containerDefinitions | length' "$TASK_DEF_FILE")
        
        log_info "Family: $FAMILY"
        log_info "CPU: $CPU, Memory: $MEMORY"
        log_info "Container definitions: $CONTAINERS"
        
        # Check if account ID is updated
        if grep -q "$AWS_ACCOUNT_ID" "$TASK_DEF_FILE"; then
            log_success "Account ID ($AWS_ACCOUNT_ID) found in task definition"
        else
            log_warning "Account ID not found in task definition - may need updating"
        fi
    else
        log_error "Task definition file is not valid JSON"
    fi
else
    log_error "Task definition file not found at $TASK_DEF_FILE"
    log_info "Create it by running the setup commands"
fi
echo

# Check GitHub Actions Workflow
echo -e "${BLUE}8. GitHub Actions Workflow${NC}"
echo "============================"
WORKFLOW_FILE=".github/workflows/ci-cd.yml"
if [ -f "$WORKFLOW_FILE" ]; then
    log_success "GitHub Actions workflow exists: $WORKFLOW_FILE"
    
    # Check if account ID is in the workflow
    if grep -q "$AWS_ACCOUNT_ID" "$WORKFLOW_FILE" 2>/dev/null; then
        log_info "Account ID found in workflow file"
    else
        log_warning "Account ID not found in workflow file - update ECR_REPOSITORY variables"
    fi
else
    log_warning "GitHub Actions workflow not found at $WORKFLOW_FILE"
    log_info "You'll need to create this file for automated deployment"
fi
echo

# Check for required GitHub Secrets (can't validate remotely, just inform)
echo -e "${BLUE}9. GitHub Secrets (Manual Check Required)${NC}"
echo "=============================================="
log_info "Please verify these secrets exist in your GitHub repository:"
log_info "  - AWS_ACCESS_KEY_ID"
log_info "  - AWS_SECRET_ACCESS_KEY"
log_info "Go to: GitHub Repository → Settings → Secrets and variables → Actions"
echo

# Summary
echo -e "${BLUE}10. Infrastructure Summary${NC}"
echo "============================="

# Count resources
TOTAL_RESOURCES=0
CREATED_RESOURCES=0

# ECS Cluster
if aws ecs describe-clusters --clusters ${APP_NAME}-cluster --region $AWS_REGION &> /dev/null; then
    CREATED_RESOURCES=$((CREATED_RESOURCES + 1))
fi
TOTAL_RESOURCES=$((TOTAL_RESOURCES + 1))

# ECR Repositories (2)
for repo in "backend" "frontend"; do
    if aws ecr describe-repositories --repository-names ${APP_NAME}-${repo} --region $AWS_REGION &> /dev/null; then
        CREATED_RESOURCES=$((CREATED_RESOURCES + 1))
    fi
    TOTAL_RESOURCES=$((TOTAL_RESOURCES + 1))
done

# CloudWatch Log Group
if aws logs describe-log-groups --log-group-name-prefix /ecs/${APP_NAME} --region $AWS_REGION | grep -q ${APP_NAME}; then
    CREATED_RESOURCES=$((CREATED_RESOURCES + 1))
fi
TOTAL_RESOURCES=$((TOTAL_RESOURCES + 1))

# IAM Roles (2)
for role in "ecsTaskExecutionRole" "ecsTaskRole"; do
    if aws iam get-role --role-name $role &> /dev/null; then
        CREATED_RESOURCES=$((CREATED_RESOURCES + 1))
    fi
    TOTAL_RESOURCES=$((TOTAL_RESOURCES + 1))
done

# Secrets (2)
for secret in "SECRET_KEY" "SENTRY_DSN"; do
    if aws secretsmanager describe-secret --secret-id ${APP_NAME}/${secret} --region $AWS_REGION &> /dev/null; then
        CREATED_RESOURCES=$((CREATED_RESOURCES + 1))
    fi
    TOTAL_RESOURCES=$((TOTAL_RESOURCES + 1))
done

echo "AWS Resources: $CREATED_RESOURCES / $TOTAL_RESOURCES created"

if [ "$CREATED_RESOURCES" -eq "$TOTAL_RESOURCES" ]; then
    log_success "All AWS infrastructure resources are created! 🎉"
    echo
    log_info "Next steps:"
    echo "  1. Set up GitHub Secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)"
    echo "  2. Create GitHub Actions workflow (.github/workflows/ci-cd.yml)"
    echo "  3. Commit and push to trigger deployment"
else
    log_warning "Some resources are missing. Check the details above."
fi

echo
echo -e "${BLUE}Infrastructure validation complete!${NC}"