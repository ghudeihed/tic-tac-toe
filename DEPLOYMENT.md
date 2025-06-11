# Ubuntu Setup Guide for AWS Deployment

## 🐧 **Ubuntu Prerequisites Setup**

### 1. **Update System Packages**
```bash
# Update package list and upgrade system
sudo apt update && sudo apt upgrade -y

# Install essential tools (if not already installed)
sudo apt install -y curl unzip wget git openssl
```

### 2. **Install AWS CLI v2** (Recommended)
```bash
# Download AWS CLI v2 for Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip the installer
unzip awscliv2.zip

# Install AWS CLI
sudo ./aws/install

# Clean up
rm -rf awscliv2.zip aws/

# Verify installation
aws --version
# Should output something like: aws-cli/2.x.x Python/3.x.x Linux/x.x.x exe/x86_64.prompt/off

# Add to PATH if needed (usually not necessary)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### 3. **Alternative: Install via Snap** (Easier but older version)
```bash
# Install AWS CLI via snap (if you prefer)
sudo snap install aws-cli --classic

# Verify
aws --version
```

### 4. **Configure AWS CLI**
```bash
# Configure AWS credentials
aws configure

# You'll be prompted for:
# AWS Access Key ID [None]: YOUR_ACCESS_KEY
# AWS Secret Access Key [None]: YOUR_SECRET_KEY
# Default region name [None]: us-east-1
# Default output format [None]: json

# Verify configuration works
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

## 🚀 **Running the Setup Script on Ubuntu**

### 1. **Prepare Your Project Directory**
```bash
# Navigate to your project (adjust path as needed)
cd ~/tic-tac-toe

# Or clone if you haven't already
# git clone https://github.com/ghudeihed/tic-tac-toe.git
# cd tic-tac-toe

# Create scripts directory
mkdir -p scripts

# Create .aws directory for task definition
mkdir -p .aws
```

### 2. **Create the Setup Script**
```bash
# Create the script file
nano scripts/setup-aws-infrastructure.sh

# Copy and paste the script content from previous response
# Save with Ctrl+X, then Y, then Enter

# Make it executable
chmod +x scripts/setup-aws-infrastructure.sh

# Verify permissions
ls -la scripts/setup-aws-infrastructure.sh
# Should show: -rwxr-xr-x ... setup-aws-infrastructure.sh
```

### 3. **Run the Setup Script**
```bash
# Execute the script
./scripts/setup-aws-infrastructure.sh

# If you get permission denied:
bash scripts/setup-aws-infrastructure.sh

# For verbose output (helpful for debugging):
bash -x scripts/setup-aws-infrastructure.sh
```

## 🔧 **Ubuntu-Specific Troubleshooting**

### **Issue: Command not found errors**
```bash
# If you get "command not found" for any tool:

# For curl:
sudo apt install curl

# For unzip:
sudo apt install unzip

# For openssl:
sudo apt install openssl

# For git:
sudo apt install git

# Install all at once:
sudo apt install -y curl unzip openssl git wget
```

### **Issue: AWS CLI not in PATH**
```bash
# Check where AWS CLI is installed
which aws

# If empty, add to PATH manually:
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc

# Or create a symlink:
sudo ln -s /usr/local/bin/aws /usr/bin/aws
```

### **Issue: Permission denied on script**
```bash
# Make sure script is executable
chmod +x scripts/setup-aws-infrastructure.sh

# Check file permissions
ls -la scripts/setup-aws-infrastructure.sh

# Run with bash if needed
bash scripts/setup-aws-infrastructure.sh
```

### **Issue: AWS credentials not configured**
```bash
# Check current configuration
aws configure list

# Reconfigure if needed
aws configure

# Check credentials file location
cat ~/.aws/credentials
cat ~/.aws/config
```

## 📋 **Complete Ubuntu Workflow**

Here's the **complete step-by-step process** for Ubuntu:

```bash
# 1. System preparation
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl unzip wget git openssl

# 2. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws/

# 3. Configure AWS
aws configure
aws sts get-caller-identity  # Verify

# 4. Navigate to project
cd ~/tic-tac-toe  # Adjust path as needed

# 5. Create directories
mkdir -p scripts .aws

# 6. Create and setup script
nano scripts/setup-aws-infrastructure.sh  # Paste the script content
chmod +x scripts/setup-aws-infrastructure.sh

# 7. Run the setup
./scripts/setup-aws-infrastructure.sh
```

## 🎯 **What Happens on Ubuntu**

The script will run natively on Ubuntu and create these AWS resources:

```bash
[INFO] 🚀 Starting AWS infrastructure setup for tic-tac-toe...

[INFO] Checking AWS CLI configuration...
[SUCCESS] AWS CLI configured for account: 123456789012

[INFO] Creating ECS cluster: tic-tac-toe-cluster
[SUCCESS] Created ECS cluster: tic-tac-toe-cluster

[INFO] Creating ECR repositories...
[SUCCESS] Created ECR repository: tic-tac-toe-backend
[SUCCESS] Created ECR repository: tic-tac-toe-frontend

... (continues with all setup steps)

[SUCCESS] AWS infrastructure setup complete! 🎉
```

## 💡 **Ubuntu-Specific Tips**

### **Using Screen/Tmux for Long Operations**
```bash
# Install screen for persistent sessions
sudo apt install screen

# Start a screen session
screen -S aws-setup

# Run your script
./scripts/setup-aws-infrastructure.sh

# Detach with Ctrl+A, D
# Reattach later with: screen -r aws-setup
```

### **Checking System Resources**
```bash
# Check available disk space
df -h

# Check memory usage
free -h

# Monitor process during script execution
htop  # Install with: sudo apt install htop
```

### **Setting Up Aliases for Convenience**
```bash
# Add helpful aliases to ~/.bashrc
echo 'alias aws-setup="./scripts/setup-aws-infrastructure.sh"' >> ~/.bashrc
echo 'alias aws-check="aws sts get-caller-identity"' >> ~/.bashrc
source ~/.bashrc

# Now you can use:
aws-setup
aws-check
```

## 🔐 **Security Considerations for Ubuntu**

### **Secure AWS Credentials Storage**
```bash
# Set proper permissions on AWS config files
chmod 600 ~/.aws/credentials
chmod 600 ~/.aws/config

# Check permissions
ls -la ~/.aws/
```

### **Using AWS CLI Profiles** (Recommended for multiple accounts)
```bash
# Configure additional profiles
aws configure --profile production
aws configure --profile staging

# Use specific profile with script
AWS_PROFILE=production ./scripts/setup-aws-infrastructure.sh

# Set default profile
export AWS_PROFILE=production
```

## ✅ **Verification Steps**

After running the script successfully on Ubuntu:

```bash
# 1. Verify AWS resources were created
aws ecs describe-clusters --clusters tic-tac-toe-cluster
aws ecr describe-repositories --repository-names tic-tac-toe-backend
aws logs describe-log-groups --log-group-name-prefix /ecs/tic-tac-toe

# 2. Check updated task definition
cat .aws/task-definition.json | grep "YOUR_ACCOUNT_ID"
# Should show your actual account ID, not the placeholder

# 3. Verify script completed successfully
echo $?  # Should output 0 (success)
```

The script works **perfectly on Ubuntu** and is actually **easier to run** than on some other systems because Ubuntu has most of the required tools pre-installed or easily available through `apt`! 🐧✨