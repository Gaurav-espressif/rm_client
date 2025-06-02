# Rainmaker CLI Tool

A powerful command-line interface tool for interacting with the Rainmaker platform, providing comprehensive device management, user authentication, and IoT operations.

## Table of Contents
- [Setup](#setup)
- [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Core Components](#core-components)
  - [Service Layer](#service-layer)
  - [Configuration Management](#configuration-management)
- [Command Reference](#command-reference)
  - [Global Options](#global-options)
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
- Internet connection for API access

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

## Architecture

### Project Structure
```
rainmakertest/
├── __init__.py
├── cli.py                 # Main CLI entry point
├── utils/                 # Utility modules
│   ├── api_client.py     # HTTP client for API communication
│   ├── config.py         # Configuration management
│   ├── config_manager.py # Advanced config handling
│   └── email_service.py  # Email service utilities
├── services/             # CLI command implementations
│   ├── auth/            # Authentication commands
│   ├── user/            # User management
│   ├── admin/           # Admin operations
│   ├── node/            # Node management
│   ├── ota/             # OTA update handling
│   ├── email/           # Email services
│   ├── server/          # Server management
│   └── create/          # Project creation tools
└── tests/               # Test suite
```

### Core Components

#### CLI Entry Point (`cli.py`)
- Implements the main command-line interface using Click
- Handles command registration and routing
- Manages global options and context
- Initializes core services and dependencies

#### API Client (`utils/api_client.py`)
- Provides HTTP communication with the Rainmaker API
- Handles authentication headers and tokens
- Manages request/response lifecycle
- Implements retry logic and error handling
- Supports multiple HTTP methods (GET, POST, PUT, DELETE)

#### Configuration Management (`utils/config.py`, `utils/config_manager.py`)
- Manages configuration files and settings
- Handles multiple configuration profiles
- Provides secure token storage
- Supports environment-specific settings

### Service Layer

#### Authentication Service
- Handles user login/logout operations
- Manages authentication tokens
- Implements session management
- Supports multiple authentication methods

#### User Service
- User account management
- Profile updates
- Password management
- User preferences

#### Node Service
- Device discovery and management
- Node status monitoring
- Parameter control
- Firmware management

#### OTA Service
- Firmware update management
- Update job scheduling
- Progress monitoring
- Rollback handling

#### Email Service
- Email verification
- Test email generation
- Notification handling
- Email template management

#### Admin Service
- Administrative operations
- User management
- System configuration
- Access control

### Configuration Management

#### File Structure
```
~/.rainmaker/
├── config.json           # Main configuration file
├── token.json           # Authentication tokens
└── logs/                # Application logs
```

#### Configuration Hierarchy
1. Command-line arguments (highest priority)
2. Environment variables
3. User configuration file
4. Default settings (lowest priority)

#### Security Features
- Secure token storage
- Environment isolation
- Configuration versioning
- Backup and recovery

### Communication Flow
```
User Input (CLI) → Command Parser → Service Layer → API Client → Rainmaker API
     ↑                                   ↓
     └───────────── Response ───────────┘
```

1. User enters command through CLI
2. Command is parsed and validated
3. Appropriate service is invoked
4. Service uses API client for communication
5. API client handles HTTP communication
6. Response is processed and formatted
7. Result is displayed to user

### Error Handling
- Comprehensive error catching
- Detailed error messages
- Debug logging
- Retry mechanisms
- Graceful degradation

### Security Considerations
- Secure token management
- SSL/TLS verification
- Configuration encryption
- Access control
- Audit logging

### Extensibility
The architecture is designed for easy extension:
- Modular service structure
- Plugin support
- Custom command registration
- Middleware capabilities
- Event system

## Command Reference

### Global Options
These options are available for all commands:
- `--debug`: Enable debug logging for detailed output
- `--config`: Specify a configuration ID (UUID) to use for the command
- `--help`: Display help information for any command

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

#### Logout
```bash
rmcli logout
```

Description: Logout current user by clearing tokens

### User Management

#### Create User
```bash
rmcli user create [OPTIONS]
```

Options:
- `--username TEXT`: Username (email or phone)
- `--password TEXT`: Password
- `--locale TEXT`: Locale preference (default: "no_locale")

#### Confirm User
```bash
rmcli user confirm [OPTIONS]
```

Options:
- `--username TEXT`: Username used during signup
- `--verification-code TEXT`: Verification code received via email/SMS
- `--locale TEXT`: Locale preference (default: "no_locale")

#### Get User Info
```bash
rmcli user info
```

Description: Get current user information

### Email Services

#### Generate Email
```bash
rmcli email generate
```

Description: Generate a new random email address

#### Verify Email
```bash
rmcli email verify [OPTIONS]
```

Options:
- `--email TEXT`: Email address to verify (uses last generated if not specified)

### Node Management

#### List Nodes
```bash
rmcli node list
```

Description: List all nodes

#### Node Status
```bash
rmcli node status [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to check status

#### Node Configuration
```bash
rmcli node config [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to get configuration

#### Update Node
```bash
rmcli node update [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to update [required]
- `--tags TEXT`: Comma-separated tags to add/update [required]

#### Map Node
```bash
rmcli node map [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to map
- `--unmap`: Unmap instead of map

#### Check Mapping Status
```bash
rmcli node mapping-status [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to check mapping status [required]
- `--request-id TEXT`: Request ID from the map operation [required]

#### Delete Node Tags
```bash
rmcli node delete-tags [OPTIONS]
```

Options:
- `--node-id TEXT`: Node ID to delete tags [required]
- `--tags TEXT`: Comma-separated tags to delete [required]

### OTA Updates

#### Image Operations

##### Upload Image
```bash
rmcli ota image upload [OPTIONS]
```

Options:
- `--base64-str TEXT`: Base64 encoded firmware image
- `--file PATH`: Path to .bin firmware file
- `--name TEXT`: Image name [required]
- `--version TEXT`: Firmware version
- `--model TEXT`: Device model
- `--type TEXT`: Device type

##### List Images
```bash
rmcli ota image list
```

Description: List all OTA images

##### Delete Image
```bash
rmcli ota image delete [OPTIONS]
```

Options:
- `--image-id TEXT`: Image ID to delete

##### Archive Image
```bash
rmcli ota image archive [OPTIONS]
```

Options:
- `--image-id TEXT`: Image ID to archive/unarchive
- `--unarchive`: Unarchive instead of archive

#### Job Operations

##### Create Job
```bash
rmcli ota job create [OPTIONS]
```

Options:
- `--name TEXT`: OTA job name
- `--image-id TEXT`: OTA image ID
- `--description TEXT`: Job description (default: "Default OTA job description")
- `--nodes TEXT`: Node IDs (comma-separated for multiple nodes)
- `--priority INTEGER`: Job priority (1-10, default: 5)
- `--timeout INTEGER`: Job timeout in seconds (default: 15 days)
- `--force`: Force push OTA
- `--approval`: Require user approval
- `--notify`: Notify end users
- `--continuous`: Keep job active after completion
- `--serialized`: Network serialized delivery

##### List Jobs
```bash
rmcli ota job list
```

Description: List OTA jobs

##### Update Job
```bash
rmcli ota job update [OPTIONS]
```

Options:
- `--job-id TEXT`: Job ID to update
- `--archive`: Archive instead of cancel

##### Job Status
```bash
rmcli ota job status [OPTIONS]
```

Options:
- `--job-id TEXT`: Job ID to check status

### Server Management

#### Update Server
```bash
rmcli server update [OPTIONS]
```

Options:
- `--endpoint TEXT`: New HTTP base URL endpoint
- `--config TEXT`: Custom config file path

#### Reset Server
```bash
rmcli server reset [OPTIONS]
```

Options:
- `--config TEXT`: Custom config file path

Description: Reset server configuration to default

#### Show Server
```bash
rmcli server show [OPTIONS]
```

Options:
- `--config TEXT`: Custom config file path

Description: Show current server endpoint

#### Cleanup
```bash
rmcli server cleanup [OPTIONS]
```

Options:
- `--days INTEGER`: Maximum age of config files in days (default: 30)

Description: Clean up old configuration files

## Use Cases

### Complete Device Management Flow
```bash
# 1. Set up server connection
rmcli server set-url --url https://api.rainmaker.com --name "Production"

# 2. Create user account
rmcli user create --email user@example.com --password secretpass --name "John Doe"

# 3. Login
rmcli login user --username user@example.com --password secretpass

# 4. Create new project
rmcli create project --name home-automation --type esp32 --template "smart-home"

# 5. List available nodes
rmcli node list --status online

# 6. Get node details
rmcli node info --node-id node123 --include-params

# 7. Control node
rmcli node control --node-id node123 --param "light" --value "on"

# 8. Create and monitor OTA update
rmcli ota create-job --image-id latest-firmware --node-ids node123 --description "Feature update"
rmcli ota monitor-job --job-id job123 --watch
```

### Automated Testing Flow
```bash
# 1. Generate test email
rmcli email generate --prefix "test_user"

# 2. Create user with generated email
rmcli user create --email <generated-email> --password "test123"

# 3. Verify email
rmcli email verify --timeout 600

# 4. Login with verified account
rmcli login user --username <generated-email> --password "test123"

# 5. Create test project
rmcli create project --name "test-project" --template "test-template"
```

## Error Handling

Common error scenarios and solutions:

### Authentication Errors (401)
- Ensure you're logged in: `rmcli login user`
- Check if token has expired: Try logging out and back in
- Verify correct credentials are being used

### Permission Errors (403)
- Ensure your user has required permissions
- Check if you're using the correct configuration
- Verify server URL is correct

### Resource Not Found (404)
- Verify resource IDs are correct
- Check if resources still exist
- Ensure you're connected to correct server

### Rate Limiting (429)
- Reduce request frequency
- Use appropriate intervals for polling
- Implement exponential backoff in scripts

### Connection Errors
- Check internet connectivity
- Verify server URL is accessible
- Check SSL certificate settings

## Support

### Getting Help
Use the `--help` flag with any command for detailed information:
```bash
# General help
rmcli --help

# Command-specific help
rmcli <command> --help

# Subcommand help
rmcli <command> <subcommand> --help
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
rmcli --debug <command>
```

### Configuration Files
- Config location: `~/.rainmaker/config.json`
- Token location: `~/.rainmaker/token.json`
- Log location: `~/.rainmaker/logs/`

### Common Tasks
- Reset configuration: Delete `~/.rainmaker/config.json`
- Clear tokens: Delete `~/.rainmaker/token.json`
- View logs: Check `~/.rainmaker/logs/`

For additional support:
1. Check the online documentation
2. Use the `--debug` flag for detailed logs
3. Contact support with debug logs if needed 