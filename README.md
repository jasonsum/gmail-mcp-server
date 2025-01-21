# Gmail Server for Model Context Protocol (MCP)

This MCP server integrates with Gmail to enable sending, removing, reading, drafting, and responding to emails.

> Note: This server enables an MCP client to read, remove, and send emails. However, the client prompts the user before conducting such activities. 

https://github.com/user-attachments/assets/5794cd16-00d2-45a2-884a-8ba0c3a90c90


## Components

### Tools

- **send-email**
  - Sends email to email address recipient 
  - Input:
    - `recipient_id` (string): Email address of addressee
    - `subject` (string): Email subject
    - `message` (string): Email content
  - Returns status and message_id

- **trash-email**
  - Moves email to trash 
  - Input:
    - `email_id` (string): Auto-generated ID of email
  - Returns success message

- **mark-email-as-read**
  - Marks email as read 
  - Input:
    - `email_id` (string): Auto-generated ID of email
  - Returns success message

- **get-unread-emails**
  - Retrieves unread emails 
  - Returns list of emails including email ID

- **read-email**
  - Retrieves given email content
  - Input:
    - `email_id` (string): Auto-generated ID of email
  - Returns dictionary of email metadata and marks email as read

- **open-email**
  - Open email in browser
  - Input:
    - `email_id` (string): Auto-generated ID of email
  - Returns success message and opens given email in default browser


## Setup

### Gmail API Setup

1. [Create a new Google Cloud project](https://console.cloud.google.com/projectcreate)
2. [Enable the Gmail API](https://console.cloud.google.com/workspace-api/products)
3. [Configure an OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) 
    - Select "external". However, we will not publish the app.
    - Add your personal email address as a "Test user".
4. Add OAuth scope `https://www.googleapis.com/auth/gmail/modify`
5. [Create an OAuth Client ID](https://console.cloud.google.com/apis/credentials/oauthclient) for application type "Desktop App"
6. Download the JSON file of your client's OAuth keys
7. Rename the key file and save it to your local machine in a secure location. Take note of the location.
    - The absolute path to this file will be passed as parameter `--creds-file-path` when the server is started. 

### Authentication

When the server is started, an authentication flow will be launched in your system browser. 
Token credentials will be subsequently saved (and later retrieved) in the absolute file path passed to parameter `--token-path`.

For example, you may use a dot directory in your home folder, replacing `[your-home-folder]`.:

| Parameter       | Example                                          |
|-----------------|--------------------------------------------------|
| `--creds-file-path` | `/[your-home-folder]/.google/client_creds.json` |
| `--token-path`      | `/[your-home-folder]/.google/app_tokens.json`    |


### Usage with Desktop App

Using [uv](https://docs.astral.sh/uv/) is recommended.

To integrate this server with Claude Desktop as the MCP Client, add the following to your app's server configuration. By default, this is stored as `~/Library/Application\ Support/Claude/claude_desktop_config.json`. 

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "uv",
      "args": [
        "--directory",
        "[absolute-path-to-git-repo]",
        "run",
        "gmail",
        "--creds-file-path",
        "[absolute-path-to-credentials-file]",
        "--token-path",
        "[absolute-path-to-access-tokens-file]"
      ]
    }
  }
}
```

The following parameters must be set
| Parameter       | Example                                          |
|-----------------|--------------------------------------------------|
| `--directory`   | Absolute path to `gmail` directory containing server |
| `--creds-file-path` | Absolute path to credentials file created in Gmail API Setup. |
| `--token-path`      | Absolute path to store and retrieve access and refresh tokens for application.  |

### Troubleshooting with MCP Inspector

To test the server, use [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector).
From the git repo, run the below changing the parameter arguments accordingly.

```bash
npx @modelcontextprotocol/inspector uv run [absolute-path-to-git-repo]/src/gmail/server.py --creds-file-path [absolute-path-to-credentials-file] --token-path [absolute-path-to-access-tokens-file]
```

