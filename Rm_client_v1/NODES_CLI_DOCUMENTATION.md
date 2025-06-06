# Rainmaker Nodes CLI Documentation

This documentation covers all available node operations in the Rainmaker CLI tool. The functionality is divided into three main categories: Basic Node Operations, Node Administration, and Node Sharing.

## Table of Contents
- [Basic Node Operations](#basic-node-operations)
- [Node Administration](#node-administration)
- [Node Sharing](#node-sharing)

## Basic Node Operations

### List User Nodes
```bash
rm nodes list
```
Lists all nodes associated with the current user.

### Get Node Configuration
```bash
rm nodes config --node-id <node_id>
```
Retrieves the configuration for a specific node.

### Get Node Status
```bash
rm nodes status --node-id <node_id>
```
Checks the online/offline status of a specific node.

### Update Node Metadata
```bash
rm nodes update --node-id <node_id> --metadata '{"key": "value"}'
```
Updates the metadata or tags for a specific node.

### Delete Node Tags
```bash
rm nodes tags delete --node-id <node_id> --tags tag1,tag2
```
Removes specified tags from a node.

### Map Node
```bash
rm nodes map --node-id <node_id> --secret-key <secret_key>
```
Maps a node to the current user's account.

### Unmap Node
```bash
rm nodes unmap --node-id <node_id> --secret-key <secret_key>
```
Unmaps a node from the current user's account.

### Check Mapping Status
```bash
rm nodes mapping-status --request-id <request_id>
```
Checks the status of a node mapping operation.

## Node Administration

### List Admin Nodes
```bash
rm nodes admin list [options]
```
Lists all nodes claimed by admin with various filtering options:
- `--node-id <node_id>`: Filter by specific node ID
- `--type <node_type>`: Filter by node type
- `--model <model>`: Filter by model
- `--fw-version <version>`: Filter by firmware version
- `--subtype <subtype>`: Filter by subtype
- `--project <project_name>`: Filter by project name
- `--status <status>`: Filter by status
- `--limit <num_records>`: Limit number of records
- `--start-id <start_id>`: Start from specific ID

### Update Admin Node
```bash
rm nodes admin update --node-id <node_id> [options]
```
Updates node metadata or tags (admin only):
- `--metadata '{"key": "value"}'`: Update metadata
- `--tags tag1,tag2`: Update tags

### Remove Admin Node Tags
```bash
rm nodes admin tags delete --node-id <node_id> --tags tag1,tag2
```
Removes specified tags from a node (admin only).

### List Admin Node Tags
```bash
rm nodes admin tags list
```
Lists all tag names used in admin's claimed nodes.

### List User-Node Associations
```bash
rm nodes admin users [--username <username>]
```
Lists user-node associations (admin view).

## Node Sharing

### Share Nodes
```bash
rm nodes share --nodes node1,node2 --username <username> [options]
```
Shares nodes with another user:
- `--primary`: Set as primary user (default: false)
- `--metadata '{"key": "value"}'`: Add sharing metadata

### Get Sharing Information
```bash
rm nodes sharing-info [--node-id <node_id>]
```
Retrieves node sharing information.

## Common Options
All commands support the following common options:
- `--help`: Show command help
- `--version`: Show API version to use (default: v1)

## Examples

1. List all your nodes:
```bash
rm nodes list
```

2. Share a node with another user:
```bash
rm nodes share --nodes node123 --username john.doe --metadata '{"access_level": "read"}'
```

3. Get filtered admin node list:
```bash
rm nodes admin list --type sensor --model v2 --limit 10
```

4. Update node metadata:
```bash
rm nodes update --node-id node123 --metadata '{"location": "living_room", "purpose": "temperature_monitoring"}'
```

5. Map a new node:
```bash
rm nodes map --node-id node123 --secret-key abc123xyz
```

## Error Handling
- All commands will return appropriate error messages if the operation fails
- Node IDs must match the pattern: `^[a-zA-Z0-9-_]+$`
- Invalid parameters or missing required fields will result in validation errors
- Authentication errors will be returned if the user doesn't have sufficient permissions

## Notes
- Some operations require admin privileges
- All metadata must be provided in valid JSON format
- Node IDs are case-sensitive
- API responses include detailed status information
- For security reasons, some operations may require additional verification 