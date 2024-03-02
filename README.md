# Discord Bot - Folder Count Tracker

This Discord bot allows you to track and display the number of folders in specified directories on your server. The bot creates and updates voice channels for each tracked folder, displaying the current folder count. Additionally, it creates total count channels for aggregated counts of specific folders.

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3 installed on your system.
- Discord account and a registered bot on the [Discord Developer Portal](https://discord.com/developers/applications).
- Bot token obtained from the Discord Developer Portal.

## Installation

1. Clone or download the repository:

   ```bash
   git clone https://github.com/sureshfizzy/Discord-folder-count-bot.git
   cd Discord-folder-count-bot
   ```

2. Install required Python packages:

   ```bash
   pip install discord.py
   ```

## Steps to Create a Discord Bot

1. **Create a Discord Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on "New Application" and give it a name.
   - Navigate to the "Bot" tab on the left sidebar.
   - Click "Add Bot" and confirm.

2. **Get the Bot Token**:
   - Under the Bot section of your application, click "Copy" to copy the bot token.
   - Keep this token secure, as it grants access to your bot.

3. **Invite the Bot to Your Server**:
   - Still in the Discord Developer Portal, navigate to the OAuth2 tab.
   - Scroll down to the "OAuth2 URL Generator" section.
   - Select the appropriate OAuth2 scopes and permissions for your bot.
   - Copy the generated OAuth2 URL and paste it into your browser.
   - Select the server where you want to add the bot and authorize it.

## Setting Up Permissions

1. **Create a Role for the Bot**:
   - In your Discord server, navigate to the server settings.
   - Click on "Roles" and then "Create Role."
   - Name the role (e.g., "Bot") and customize its permissions.

2. **Grant Necessary Permissions**:
   - Assign the bot role the necessary permissions based on the bot's functionality.
   - Ensure that the bot has permissions to read and send messages in the channels where it will operate.
   - Grant additional permissions as needed, such as managing messages, embedding links, etc.

3. **Assign the Bot Role**:
   - Go to the member list in your server.
   - Find the bot's username and click on it.
   - Assign the bot role you created to the bot.

4. **Test Permissions**:
   - Test the bot's permissions by running it in your server.
   - Make sure it can perform its intended actions without any issues.
  
## Configuration

1. Open `discord_bot.py` in a text editor.

2. Replace `'YOUR_TOKEN'` with the actual bot token obtained from the Discord Developer Portal:

   ```python
   TOKEN = 'YOUR_TOKEN'
   ```

3. Update the `folders` dictionary with the folders you want to track and their corresponding paths:

   ```python
   folders = {
       "Movies": "/path/to/Movies",
       "Movies2": "/path/to/Movies",
       "Series": "/path/to/Series",
       "Series2": "/path/to/Series",
       # Add other folders with their paths here
   }
   ```

## Running the Bot

### On Ubuntu

1. Open a terminal and navigate to the bot directory.

2. Run the bot using the following command:

   ```bash
   python3 discord_bot.py
   ```

3. The bot will start running and will print "Bot is ready" once it is connected to Discord.

### Running as a System Service (Ubuntu)

1. Create a service file for the bot:

   ```bash
   sudo nano /etc/systemd/system/discord-bot.service
   ```

2. Add the following configuration to the file (modify paths accordingly):

   ```ini
   [Unit]
   Description=Discord Bot - Folder Count Tracker
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/discord_bot.py
   WorkingDirectory=/path/to/discord-bot-directory
   Restart=always
   User=your_username
   Group=your_group

   [Install]
   WantedBy=default.target
   ```

3. Save the file and exit the text editor.

4. Start the service:

   ```bash
   sudo systemctl start discord-bot
   ```

5. Enable the service to start on boot:

   ```bash
   sudo systemctl enable discord-bot
   ```

Now, your Discord bot will run as a system service.

## Permissions

Ensure the bot has the necessary permissions on your Discord server:

1. Create a new role for the bot.
2. Assign the role the following permissions:
   - Read Messages
   - Send Messages
   - Connect
   - View Channel

3. Add the bot to your server and assign the role to the bot.

4. The bot should now have the required permissions to create and manage channels.

## Usage

Once the bot is running and added to your server, it will automatically create and update channels in the specified category. The channels will display the current count of folders in the tracked directories. The bot updates counts every 24 hours (You can update the delay according to your needs).
