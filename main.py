import os
import re
import discord
from tkinter import Tk, filedialog
import textwrap

# Discord setup
BOT_TOKEN = '<BOT TOKEN>'  # Replace with your bot token
FORUM_CHANNEL_ID = 1234567890  # Replace with your forum channel ID
THREAD_ID = 11234567890  # Replace with your thread ID


intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


def format_guide(file_path):
    """Formats the guide for Discord posting."""
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()

        # Split YAML header and body
        if "---" in content:
            parts = content.split("---", 2)
            yaml_header = parts[1]
            body = parts[2]
        else:
            yaml_header = ""
            body = content

        # Extract tags from YAML
        tags_match = re.search(r"tags:\s*\[([^\]]+)\]", yaml_header, re.IGNORECASE)
        tags = tags_match.group(1).replace(",", ", ") if tags_match else None

        # Format the content with or without tags
        if tags:
            formatted_content = f"Tags: {tags}\n\n{body.strip()}"
        else:
            formatted_content = body.strip()

        print(f"Formatted content preview:\n{formatted_content[:500]}")  # Debugging: Print first 500 chars
        return formatted_content
    except Exception as e:
        print(f"Error formatting guide: {e}")
        return None



def clean_markdown(content):
    """Clean unsupported Markdown, prevent embeds, and fix formatting for Discord."""
    # Remove image placeholders like ![[Pasted image ...]]
    content = re.sub(r'!\[\[.*?\]\]', '', content)

    # Replace internal link placeholders [[Title|link]] with plain text
    content = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', content)

    # Replace any remaining unsupported Markdown
    content = re.sub(r'\[\[.*?\]\]', '', content)

    # Disable embeds for all URLs
    def disable_embed(match):
        url = match.group(0)
        return f"{url} \u200B"  # Add a space, then zero-width space, after the URL

    content = re.sub(r'(https?://[^\s]+)', disable_embed, content)

    # Remove unnecessary blank lines (two or more consecutive newlines)
    content = re.sub(r'\n\s*\n', '\n', content)

    # Remove '---' separators
    content = re.sub(r'^\s*-{3,}\s*$', '', content, flags=re.MULTILINE)

    return content.strip()  # Remove leading/trailing whitespace


async def post_to_thread(formatted_content):
    """Posts the cleaned content to a specific thread."""
    try:
        # Clean Markdown content for Discord
        cleaned_content = clean_markdown(formatted_content)

        # Get the thread by ID
        thread = await client.fetch_channel(THREAD_ID)
        if not isinstance(thread, discord.Thread):
            print(f"Channel with ID {THREAD_ID} is not a thread.")
            return

        # Split content into logical chunks, respecting Markdown structure
        chunks = []
        current_chunk = ""
        for line in cleaned_content.splitlines():
            if len(current_chunk) + len(line) + 1 > 2000:  # Check chunk size
                chunks.append(current_chunk.strip())
                current_chunk = ""
            current_chunk += line + "\n"

        # Add the final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Post each chunk
        for idx, chunk in enumerate(chunks):
            print(f"Posting chunk {idx + 1}/{len(chunks)}: {chunk[:100]}...")
            await thread.send(content=chunk)

        print(f"Content posted successfully to thread '{thread.name}'.")
    except discord.HTTPException as http_err:
        print(f"HTTPException: {http_err}")
    except Exception as e:
        print(f"Error posting to thread: {e}")


def main():
    # Select file
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a Guide File", filetypes=[("Markdown Files", "*.md")])
    if not file_path:
        print("No file selected. Exiting.")
        return

    # Format content
    formatted_content = format_guide(file_path)
    if not formatted_content:
        print("Failed to format the guide.")
        return

    # Post to thread
    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        await post_to_thread(formatted_content)
        await client.close()  # Shut down after posting

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
