# keep-mcp
MCP server for Google Keep

A simple Python project that demonstrates the usage of the Google Keep API using gkeepapi.

## Setup

1. Install Python dependencies using `uv`:
```bash
uv pip install .
```

2. Set up your environment variables:
   - Copy `.example.env` to `.env`:
   ```bash
   cp .example.env .env
   ```
   - Update the `.env` file with your Google account credentials:
     - `GOOGLE_EMAIL`: Your Google account email
     - `GOOGLE_MASTER_TOKEN`: Your Google account master token

   To get your master token, you can use the following Docker command:
   ```bash
   docker run --rm -it --entrypoint /bin/sh python:3 -c 'pip install gpsoauth; python3 -c '\''print(__import__("gpsoauth").exchange_token(input("Email: "), input("OAuth Token: "), input("Android ID: ")))'\'
   ```

## Usage

To run the project:
```bash
python main.py
```

## Note
This is a basic example that demonstrates how to connect to Google Keep API and retrieve notes. Make sure to handle your credentials securely in a production environment.

## Environment Variables
The following environment variables are required:
- `GOOGLE_EMAIL`: Your Google account email address
- `GOOGLE_MASTER_TOKEN`: Your Google account master token

Check https://gkeepapi.readthedocs.io/en/latest/#obtaining-a-master-token and https://github.com/simon-weber/gpsoauth?tab=readme-ov-file#alternative-flow for more information.

These should be set in your `.env` file. Never commit the `.env` file to version control.

## Troubleshooting

- If you get "DeviceManagementRequiredOrSyncDisabled" check https://admin.google.com/ac/devices/settings/general and turn "Turn off mobile management (Unmanaged)"
