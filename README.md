# Rainmaker CLI Tool

A powerful command-line interface tool for interacting with the Rainmaker platform, providing comprehensive device management, user authentication, and IoT operations.

## Table of Contents
- [Setup](#setup)
- [Command Reference](#command-reference)
  - [Authentication Commands](#authentication-commands)
  - [User Management](#user-management)
  - [Node Management](#node-management)
  - [OTA Updates](#ota-updates)
  - [Email Services](#email-services)
  - [Server Management](#server-management)
  - [Creation Tools](#creation-tools)
- [Use Cases](#use-cases)
- [Error Handling](#error-handling)
- [Support](#support)

## Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rm_client
```

2. Install the package in development mode:
```bash
pip install -e .
```

### Configuration
The CLI tool uses configuration files stored in your home directory:
- `~/.rainmaker/config.json` - For server configuration
- `~/.rainmaker/token.json` - For authentication tokens

## Command Reference

### Global Options
- `--debug`: Enable debug logging
- `--config`: Specify a configuration ID (UUID) to use for the command

### Authentication Commands

#### Login
```bash
rmcli login user [OPTIONS]
```

Options:
- `--username TEXT`: Username (email or phone)
- `--password TEXT`: User password
- `--endpoint TEXT`: Server endpoint URL

Examples:
```bash
# Interactive login
rmcli login user

# Login with credentials
rmcli login user --username user@example.com --password secretpass

# Login with custom endpoint
rmcli login user --username user@example.com --password secretpass --endpoint https://custom.api.com
```

Use Cases:
- First-time user authentication
- Switching between different server environments
- Creating new configuration profiles

#### Logout
```bash
rmcli logout
```

Use Cases:
- Securely ending a session
- Clearing authentication tokens
- Switching between different user accounts

### Email Services

#### Generate Email
```bash
rmcli email generate
```

Generates a random email address for testing purposes.

Example:
```bash
rmcli email generate
# Output: Email address generated: test_user_123@example.com
```

#### Verify Email
```bash
rmcli email verify [OPTIONS]
```

Options:
- `--email TEXT`: Email address to verify (uses last generated if not specified)

Examples:
```bash
# Verify last generated email
rmcli email verify

# Verify specific email
rmcli email verify --email user@example.com
```

Use Cases:
- Testing email verification flow
- Retrieving verification codes
- Automated testing of user registration

### Node Management

#### List Nodes
```bash
rmcli node list [OPTIONS]
```

Options:
- `--status TEXT`: Filter nodes by status
- `--type TEXT`: Filter nodes by type

Examples:
```bash
# List all nodes
rmcli node list

# List online nodes
rmcli node list --status online

# List specific type of nodes
rmcli node list --type esp32
```

#### Node Information
```bash
rmcli node info [OPTIONS]
```

Options:
- `--node-id TEXT`: ID of the node [required]
- `--format TEXT`: Output format (json|table)

Examples:
```bash
# Get node details
rmcli node info --node-id node123

# Get node details in JSON format
rmcli node info --node-id node123 --format json
```

### OTA Updates

#### List OTA Images
```bash
rmcli ota list-images [OPTIONS]
```

Options:
- `--type TEXT`: Filter by image type
- `--version TEXT`: Filter by version

Examples:
```bash
# List all images
rmcli ota list-images

# List specific version
rmcli ota list-images --version 1.0.0
```

#### Create OTA Job
```bash
rmcli ota create-job [OPTIONS]
```

Options:
- `--image-id TEXT`: ID of the OTA image [required]
- `--node-ids TEXT`: Comma-separated list of node IDs [required]
- `--schedule TEXT`: Schedule time for the update

Examples:
```bash
# Create immediate update job
rmcli ota create-job --image-id img123 --node-ids node1,node2

# Create scheduled update job
rmcli ota create-job --image-id img123 --node-ids node1,node2 --schedule "2024-03-20 10:00:00"
```

### Server Management

#### Set Server URL
```bash
rmcli server set-url [OPTIONS]
```

Options:
- `--url TEXT`: Server URL [required]
- `--verify-ssl BOOLEAN`: Whether to verify SSL certificates

Examples:
```bash
# Set production server
rmcli server set-url --url https://api.rainmaker.com

# Set development server without SSL verification
rmcli server set-url --url https://dev-api.rainmaker.com --verify-ssl false
```

#### Get Server Info
```bash
rmcli server info
```

Displays current server configuration and status.

### Creation Tools

#### Create Project
```bash
rmcli create project [OPTIONS]
```

Options:
- `--name TEXT`: Project name [required]
- `--type TEXT`: Project type
- `--template TEXT`: Template to use

Examples:
```bash
# Create basic project
rmcli create project --name my-project

# Create project from template
rmcli create project --name my-project --template esp32-basic
```

## Use Cases

### Device Provisioning Flow
```bash
# 1. Set up server connection
rmcli server set-url --url https://api.rainmaker.com

# 2. Create user account
rmcli user create --email user@example.com --password secretpass

# 3. Login
rmcli login user --username user@example.com --password secretpass

# 4. Create new project
rmcli create project --name home-automation

# 5. Add and configure node
rmcli node add --type esp32 --name "Living Room Light"

# 6. Update firmware
rmcli ota create-job --image-id latest-firmware --node-ids node123
```

### User Management Flow
```bash
# 1. Generate test email
rmcli email generate

# 2. Create user with generated email
rmcli user create --email <generated-email>

# 3. Verify email
rmcli email verify

# 4. Login with verified account
rmcli login user --username <generated-email> --password secretpass
```

## Error Handling

If you encounter any errors:
1. Use the `--debug` flag for detailed logging
2. Ensure you're logged in for commands that require authentication
3. Verify your server configuration is correct
4. Check your internet connection

Common Error Codes:
- `401`: Authentication required
- `403`: Insufficient permissions
- `404`: Resource not found
- `429`: Rate limit exceeded

## Support

For additional help, use the `--help` flag with any command:
```bash
rmcli --help
rmcli <command> --help
rmcli <command> <subcommand> --help
```

### Getting Help with Specific Commands
```bash
# Get help with login
rmcli login --help

# Get help with OTA updates
rmcli ota --help

# Get help with node management
rmcli node --help
``` 