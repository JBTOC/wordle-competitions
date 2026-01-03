# MCP Integration Guide: Secure JIRA & GitHub Access

This guide explains how to set up secure, read-only access to JIRA and GitHub using Model Context Protocol (MCP) servers with API tokens.

## Overview

MCP (Model Context Protocol) allows AI assistants to securely access external services through standardized server implementations. This approach provides:

- **Security**: Credentials stored locally, never sent to AI providers
- **Auditability**: All API calls logged locally
- **Control**: Easy to enable/disable access
- **Scope Limitation**: Read-only access via token permissions

## Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────┐
│   Cline     │ ◄─────► │ MCP Server  │ ◄─────► │  JIRA    │
│  (AI Tool)  │         │  (Local)    │         │  GitHub  │
└─────────────┘         └─────────────┘         └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │ API Keys │
                        │ (Local)  │
                        └──────────┘
```

## Prerequisites

- Node.js 18+ installed
- Access to JIRA Cloud instance
- GitHub account
- Cline extension in VSCode

## Step 1: Generate API Tokens

### JIRA API Token

1. Log in to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a descriptive name: "MCP Read-Only Access"
4. Copy the token immediately (you won't see it again)
5. Store securely - we'll use it in configuration

**Token Format**: `ATATT3xFfGF0...` (base64 string)

### GitHub Personal Access Token (PAT)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name: "MCP Read-Only Access"
4. Set expiration (recommend 90 days for security)
5. Select **read-only** scopes:
   - `repo` → `public_repo` (for public repos only)
   - OR `repo` (full) if you need private repo access
   - `read:org` (to read organization data)
   - `read:user` (to read user profile)
   - `read:project` (to read projects)
6. Click "Generate token"
7. Copy the token immediately

**Token Format**: `ghp_...` (starts with ghp_)

## Step 2: Install MCP Servers

### Option A: Using Official MCP Servers (Recommended)

```bash
# Install GitHub MCP server
npm install -g @modelcontextprotocol/server-github

# Install JIRA MCP server (if available)
# Note: Check https://github.com/modelcontextprotocol for official servers
```

### Option B: Using Community Servers

```bash
# Search for community MCP servers
npm search mcp-server-jira
npm search mcp-server-github
```

### Option C: Create Custom MCP Server (Advanced)

If official servers don't exist, you can create a simple MCP server. See `custom-mcp-server/` directory for examples.

## Step 3: Configure MCP in Cline

### Locate Cline Configuration

The MCP configuration file is located at:
- **macOS**: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Linux**: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Windows**: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

### Configuration Structure

Create or edit the `cline_mcp_settings.json` file:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN_HERE"
      }
    },
    "jira": {
      "command": "node",
      "args": [
        "/path/to/custom-mcp-server/jira-server.js"
      ],
      "env": {
        "JIRA_HOST": "your-domain.atlassian.net",
        "JIRA_EMAIL": "your-email@example.com",
        "JIRA_API_TOKEN": "ATATT3xFfGF0_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

## Step 4: Secure Credential Storage

### Best Practices

1. **Never commit tokens to git**
   - Add `cline_mcp_settings.json` to `.gitignore`
   - Use environment variables for sensitive data

2. **Use environment variables** (More Secure)

Create a `.env` file in your home directory:

```bash
# ~/.mcp_credentials
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
export JIRA_API_TOKEN="ATATT3xFfGF0..."
export JIRA_EMAIL="your-email@example.com"
export JIRA_HOST="your-domain.atlassian.net"
```

Then source it before starting VSCode:
```bash
source ~/.mcp_credentials && code
```

3. **Use macOS Keychain** (macOS Only)

```bash
# Store tokens in keychain
security add-generic-password -a "$USER" -s "mcp-github-token" -w "ghp_..."
security add-generic-password -a "$USER" -s "mcp-jira-token" -w "ATATT3xFfGF0..."

# Retrieve in MCP config using a wrapper script
```

4. **File Permissions**

```bash
# Restrict access to config file
chmod 600 ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

## Step 5: Available MCP Tools

Once configured, the following tools become available:

### GitHub Tools
- `github_search_repositories` - Search for repositories
- `github_get_file_contents` - Read file contents
- `github_list_commits` - List commit history
- `github_search_issues` - Search issues and PRs
- `github_get_issue` - Get issue details
- `github_list_issues` - List repository issues

### JIRA Tools (Custom Implementation)
- `jira_search_issues` - Search JIRA issues (JQL)
- `jira_get_issue` - Get issue details
- `jira_list_projects` - List accessible projects
- `jira_get_project` - Get project details

## Step 6: Testing the Integration

### Test GitHub Access

1. Switch to Advance mode in Cline
2. Ask: "Can you search for repositories related to 'wordle' on GitHub?"
3. Verify the MCP server responds with results

### Test JIRA Access

1. Ask: "Can you search for JIRA issues in project XYZ?"
2. Verify the MCP server connects and returns issues

### Troubleshooting

Check MCP server logs:
```bash
# Logs are typically in VSCode's output panel
# View → Output → Select "MCP Servers" from dropdown
```

Common issues:
- **Authentication failed**: Check token validity and permissions
- **Server not starting**: Verify Node.js installation and server path
- **No tools available**: Restart VSCode after configuration changes

## Security Considerations

### ✅ Security Best Practices

1. **Token Scope**: Use minimum required permissions (read-only)
2. **Token Expiration**: Set expiration dates (90 days recommended)
3. **Token Rotation**: Regularly rotate tokens
4. **Audit Logging**: Monitor MCP server logs for unusual activity
5. **Network Security**: MCP servers run locally, no external exposure
6. **Credential Storage**: Never commit tokens to version control

### ⚠️ Security Warnings

1. **AI Provider Access**: The AI (Claude/OpenAI) never sees your tokens
2. **Local Processing**: All API calls originate from your machine
3. **Rate Limits**: Respect API rate limits to avoid account issues
4. **Shared Machines**: Don't use on shared/public computers
5. **Token Leakage**: If tokens are compromised, revoke immediately

### 🔒 Token Revocation

**If tokens are compromised:**

1. **GitHub**: https://github.com/settings/tokens → Delete token
2. **JIRA**: https://id.atlassian.com/manage-profile/security/api-tokens → Revoke token
3. **Update Config**: Remove from MCP configuration
4. **Generate New**: Create new tokens with fresh names

## Advanced Configuration

### Custom MCP Server Example

See `custom-mcp-server/jira-server.js` for a complete implementation example.

### Proxy Configuration

If behind a corporate proxy:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_...",
        "HTTP_PROXY": "http://proxy.company.com:8080",
        "HTTPS_PROXY": "http://proxy.company.com:8080"
      }
    }
  }
}
```

### Multiple JIRA Instances

```json
{
  "mcpServers": {
    "jira-work": {
      "command": "node",
      "args": ["/path/to/jira-server.js"],
      "env": {
        "JIRA_HOST": "work.atlassian.net",
        "JIRA_EMAIL": "work@example.com",
        "JIRA_API_TOKEN": "token1"
      }
    },
    "jira-personal": {
      "command": "node",
      "args": ["/path/to/jira-server.js"],
      "env": {
        "JIRA_HOST": "personal.atlassian.net",
        "JIRA_EMAIL": "personal@example.com",
        "JIRA_API_TOKEN": "token2"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Search JIRA Issues

```
User: "Show me all open bugs in project WORD assigned to me"

Bob: [Uses jira_search_issues with JQL: "project = WORD AND type = Bug AND status = Open AND assignee = currentUser()"]
```

### Example 2: Review GitHub PR

```
User: "What changes were made in PR #123 of my wordle repo?"

Bob: [Uses github_get_issue and github_get_file_contents to analyze the PR]
```

### Example 3: Cross-Reference

```
User: "Find all GitHub issues that reference JIRA ticket WORD-123"

Bob: [Searches GitHub issues for "WORD-123" and correlates with JIRA data]
```

## Maintenance

### Regular Tasks

- **Weekly**: Review MCP server logs for errors
- **Monthly**: Rotate API tokens
- **Quarterly**: Review and update token permissions
- **Annually**: Audit all active tokens and revoke unused ones

### Monitoring

Create a simple monitoring script:

```bash
#!/bin/bash
# check-mcp-health.sh

echo "Checking GitHub token..."
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
     https://api.github.com/user | jq '.login'

echo "Checking JIRA token..."
curl -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
     "https://$JIRA_HOST/rest/api/3/myself" | jq '.displayName'
```

## Support and Resources

- **MCP Documentation**: https://modelcontextprotocol.io
- **GitHub API**: https://docs.github.com/en/rest
- **JIRA API**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Cline MCP Guide**: Check Cline documentation for latest MCP features

## Conclusion

This setup provides secure, auditable, read-only access to JIRA and GitHub through MCP servers. The AI assistant can now help you with:

- Searching and analyzing JIRA issues
- Reviewing GitHub repositories and code
- Cross-referencing tickets and commits
- Generating reports from both systems

All while keeping your credentials secure and under your control.