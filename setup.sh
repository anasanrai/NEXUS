#!/bin/bash

# NEXUS Setup Script for Ubuntu 24.04
# This script installs and configures NEXUS autonomous AI system
# Run with: sudo bash setup.sh

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

# Check Ubuntu version
if ! grep -q "Ubuntu 24" /etc/os-release; then
    log_warning "This script is designed for Ubuntu 24.04. Your system may not be fully compatible."
fi

log_info "Starting NEXUS setup for Ubuntu 24.04..."
log_info "This may take several minutes. Please be patient."

# Function to check command success
check_command() {
    if [ $? -eq 0 ]; then
        log_success "$1"
    else
        log_error "$1 failed"
        exit 1
    fi
}

# 1. Update system and install basic dependencies
log_info "Step 1: Updating system and installing basic dependencies..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y software-properties-common curl wget git build-essential
check_command "System update and basic packages"

# 2. Install Python 3.12
log_info "Step 2: Installing Python 3.12..."
if ! command -v python3.12 &> /dev/null; then
    sudo apt install -y python3.12 python3.12-venv python3.12-dev python3.12-pip
    check_command "Python 3.12 installation"
else
    log_success "Python 3.12 already installed"
fi

# Verify Python version
PYTHON_VERSION=$(python3.12 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ "$PYTHON_VERSION" != "3.12" ]]; then
    log_error "Python 3.12 not found. Current version: $PYTHON_VERSION"
    exit 1
fi
log_success "Python 3.12 verified: $PYTHON_VERSION"

# 3. Create virtual environment
log_info "Step 3: Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3.12 -m venv venv
    check_command "Virtual environment creation"
else
    log_success "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
check_command "Virtual environment activation"

# Upgrade pip
pip install --upgrade pip
check_command "Pip upgrade"

# 4. Install Python requirements
log_info "Step 4: Installing Python requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    check_command "Python requirements installation"
else
    log_error "requirements.txt not found"
    exit 1
fi

# 5. Install Playwright browsers
log_info "Step 5: Installing Playwright browsers..."
if command -v playwright &> /dev/null; then
    playwright install
    check_command "Playwright browsers installation"
else
    log_warning "Playwright not found in requirements. Installing manually..."
    pip install playwright
    playwright install
    check_command "Playwright installation and browsers"
fi

# 6. Install and setup Docker
log_info "Step 6: Installing and setting up Docker..."
if ! command -v docker &> /dev/null; then
    # Install Docker
    sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    check_command "Docker installation"

    # Add user to docker group
    sudo usermod -aG docker $USER
    log_warning "Added $USER to docker group. You may need to log out and back in for this to take effect."
else
    log_success "Docker already installed"
fi

# Start Docker service
sudo systemctl enable docker
sudo systemctl start docker
check_command "Docker service start"

# 7. Setup Redis with Docker
log_info "Step 7: Setting up Redis with Docker..."
if ! docker ps | grep -q redis; then
    # Stop any existing redis container
    docker stop redis-nexus 2>/dev/null || true
    docker rm redis-nexus 2>/dev/null || true

    # Run Redis container with persistence
    docker run -d \
        --name redis-nexus \
        --restart unless-stopped \
        -p 6379:6379 \
        -v redis-data:/data \
        redis:7-alpine redis-server --appendonly yes
    check_command "Redis container setup"

    # Wait for Redis to be ready
    log_info "Waiting for Redis to be ready..."
    sleep 5
    if docker exec redis-nexus redis-cli ping | grep -q PONG; then
        log_success "Redis is ready"
    else
        log_error "Redis failed to start properly"
        exit 1
    fi
else
    log_success "Redis container already running"
fi

# 8. Setup environment file
log_info "Step 8: Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_success "Created .env from .env.example"
        log_warning "Please edit .env file with your actual API keys and configuration"
        echo ""
        echo "Required environment variables to configure:"
        echo "- OPENROUTER_API_KEY"
        echo "- TAVILY_API_KEY"
        echo "- SUPABASE_URL"
        echo "- SUPABASE_KEY"
        echo "- TELEGRAM_BOT_TOKEN"
        echo "- TELEGRAM_CHAT_ID"
        echo "- REDIS_URL (set to redis://localhost:6379)"
        echo ""
        echo "Optional:"
        echo "- STRIPE_SECRET_KEY (for payments)"
        echo "- GITHUB_TOKEN (for Git operations)"
        echo "- WORDPRESS_* (for blogging)"
        echo "- TWITTER_*, LINKEDIN_*, INSTAGRAM_* (for social media)"
    else
        log_error ".env.example not found"
        exit 1
    fi
else
    log_success ".env file already exists"
fi

# Set Redis URL if not set
if ! grep -q "REDIS_URL" .env; then
    echo "REDIS_URL=redis://localhost:6379" >> .env
    log_success "Added Redis URL to .env"
fi

# 9. Set file permissions
log_info "Step 9: Setting file permissions..."
chmod +x main.py
chmod +x validate_system.py
chmod +x setup.sh 2>/dev/null || true
check_command "File permissions setup"

# 10. Create systemd service
log_info "Step 10: Creating systemd service for auto-restart..."
SERVICE_FILE="/etc/systemd/system/nexus.service"
WORKING_DIR=$(pwd)
USER_NAME=$(whoami)

sudo tee $SERVICE_FILE > /dev/null << EOF
[Unit]
Description=NEXUS Autonomous AI Operating System
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$WORKING_DIR
Environment=PATH=$WORKING_DIR/venv/bin
ExecStart=$WORKING_DIR/venv/bin/python3 $WORKING_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes

# Resource limits
MemoryLimit=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
EOF

check_command "Systemd service creation"

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable nexus.service
check_command "Systemd service enable"

# 11. Run health check
log_info "Step 11: Running system health check..."
if [ -f "validate_system.py" ]; then
    source venv/bin/activate
    python3 validate_system.py
    if [ $? -eq 0 ]; then
        log_success "Health check passed!"
    else
        log_warning "Health check failed. Please check the output above."
    fi
else
    log_error "validate_system.py not found"
    exit 1
fi

# 12. Final instructions
log_success "NEXUS setup completed successfully!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 NEXUS is now installed and configured!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Start NEXUS manually for testing:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "3. Or start the systemd service:"
echo "   sudo systemctl start nexus"
echo ""
echo "4. Check service status:"
echo "   sudo systemctl status nexus"
echo ""
echo "5. View logs:"
echo "   sudo journalctl -u nexus -f"
echo ""
echo "6. Stop service:"
echo "   sudo systemctl stop nexus"
echo ""
echo "🔧 Useful Commands:"
echo "- Restart: sudo systemctl restart nexus"
echo "- Logs: sudo journalctl -u nexus -f"
echo "- Status: sudo systemctl status nexus"
echo ""
echo "📚 Documentation:"
echo "- README.md - Feature overview"
echo "- SETUP.md - Configuration guide"
echo "- QUICKSTART.md - Getting started"
echo ""
echo "⚠️  Important Notes:"
echo "- You may need to log out and back in for Docker group changes"
echo "- Configure all API keys in .env before starting"
echo "- Redis data persists in Docker volume 'redis-data'"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Deactivate virtual environment
deactivate

log_success "Setup script completed. NEXUS is ready to run!"