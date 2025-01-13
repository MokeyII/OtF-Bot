# OtF-Bot
Obsidian.md to Discord Forum Python script

This project is a Python script that allows you to upload formatted Obsidian markdown notes to a Discord forum thread. It processes `.md` files, cleans unsupported Markdown, and ensures compatibility with Discord formatting.

---

## Features

- **YAML Metadata Support:** Extracts tags from YAML front matter for inclusion in the post.
- **Markdown Cleanup:** Removes unsupported Markdown syntax and unwanted elements.
- **Discord Integration:** Posts formatted content to a specified Discord thread in chunks that fit Discord's character limit.

---

## Prerequisites

- **Python 3.8+**
- **Libraries:** Install required Python libraries using:
  ```bash
  pip install discord.py tkinter
  ```
- **Discord Bot Token:** Set up a bot and retrieve its token.
- **Forum Channel and Thread ID:** Gather IDs for the forum channel and the specific thread where posts will be made.

---

## Discord Developer Setup

1. **Create a Discord Application:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and name it.

2. **Add a Bot:**
   - In the application settings, navigate to the **Bot** section.
   - Click **Add Bot** and confirm.

3. **Set Bot Permissions:**
   - Under the **OAuth2** tab, generate an invite link with the required permissions:
     - `Manage Messages`
     - `Read Messages/View Channels`
     - `Send Messages`

4. **Invite the Bot:**
   - Use the generated OAuth2 URL to invite the bot to your Discord server.

5. **Retrieve IDs:**
   - Enable **Developer Mode** in Discord (Settings > Advanced).
   - Right-click your channel or thread and select **Copy ID**.

---

## How to Install and Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/obsidian-to-discord.git
   cd obsidian-to-discord
   ```

2. **Update Configuration:**
   - Open the script file and replace placeholders:
     - `<BOT TOKEN>`: Your Discord bot token.
     - `FORUM_CHANNEL_ID`: The ID of the forum channel.
     - `THREAD_ID`: The ID of the thread.

3. **Run the Script:**
   ```bash
   python main.py
   ```

4. **Select a File:**
   - A file dialog will appear. Select the Markdown file (`.md`) to post.

5. **Check Results:**
   - The bot will format and post the content to the specified Discord thread. Logs will indicate success or errors.

---

## Notes

- **Chunking:** If the content exceeds Discord's message limit (2,000 characters), it will be split into multiple posts.
- **Content Preview:** Logs will display a preview of the content for verification.
- **Closing:** The bot will automatically shut down after posting.

---

## Contribution

Feel free to fork, submit issues, or create pull requests to improve the script.

---
