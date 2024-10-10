import random
import string
import datetime
import json
import os
import telebot

from keep_alive import keep_alive
keep_alive()

# Configuration
TOKEN = "7001355572:AAFAqeNWStcmPry4Zap8u0LXZAAPS-5AVgc"  # Replace with your bot token
ADMIN_IDS = [6906270448]  # Admin ID(s) as integers
USER_FILE = "users.json"
KEY_FILE = "keys.json"

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Load keys and users from JSON files
def load_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            keys = json.load(f)
    else:
        keys = {}

    return users, keys

# Save keys and users to JSON files
def save_data(users, keys):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)
    with open(KEY_FILE, 'w') as f:
        json.dump(keys, f)

# Generate a random key
def generate_key(length=11):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Add time to the current date
def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

# Initialize keys and users
users, keys = load_data()

# Start command
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝐐 𝐫𝐞 𝐂𝐇𝐀𝐏𝐑𝐈, {user_name}! 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐘𝐎𝐔𝐑 𝐅𝐀𝐓𝐇𝐑𝐄𝐑𝐒 𝐁𝐨𝐓 𝐒𝐞𝐫𝐯𝐢𝐜𝐞.
🤖𝐀𝐍𝐏𝐀𝐃 𝐔𝐒𝐄 𝐇𝐄𝐋𝐏 𝐂𝐎𝐌𝐌𝐀𝐍𝐃: /help
'''
    bot.reply_to(message, response)

# Rules command
@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐅𝐎𝐋𝐋𝐎𝐖 𝐓𝐇𝐈𝐒 𝐑𝐔𝐋𝐄𝐒 𝐄𝐋𝐒𝐄 𝐘𝐎𝐔𝐑 𝐌𝐎𝐓𝐇𝐄𝐑 𝐈𝐒 𝐌𝐈𝐍𝐄:
1. 𝐍𝐨 𝐒𝐩𝐚𝐦.
2. 𝐁𝐞 𝐑𝐞𝐬𝐩𝐞𝐜𝐭𝐟𝐮𝐥.
3. 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐜𝐨𝐫𝐫𝐞𝐜𝐭𝐥𝐲.
'''
    bot.reply_to(message, response)

# Generate key command
@bot.message_handler(commands=['genkey'])
def generate_key_command(message):
    user_id = str(message.chat.id)
    if user_id in map(str, ADMIN_IDS):
        command = message.text.split()
        if len(command) == 3:
            try:
                time_amount = int(command[1])
                time_unit = command[2].lower()
                if time_unit == 'hours':
                    expiration_date = add_time_to_current_date(hours=time_amount)
                elif time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")

                key = generate_key()
                keys[key] = expiration_date
                save_data(users, keys)
                response = f"𝐋𝐢𝐜𝐞𝐧𝐬𝐞: {key}\n𝐄𝐬𝐩𝐢𝐫𝐞𝐬 𝐎𝐧: {expiration_date}\n𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐅𝐨𝐫 1 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐀𝐜𝐜𝐨𝐮𝐧𝐭"
            except ValueError:
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐩𝐞𝐜𝐢𝐟𝐲 𝐀 𝐕𝐚𝐥𝐢𝐝 𝐍𝐮𝐦𝐛𝐞𝐫 𝐚𝐧𝐝 𝐮𝐧𝐢𝐭 𝐨𝐟 𝐓𝐢𝐦𝐞 (hours/days)."
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /genkey <amount> <hours/days>"
    else:
        response = "𝐎𝐧𝐥𝐲 𝐏𝐚𝐩𝐚 𝐎𝐟 𝐛𝐨𝐭 𝐜𝐚𝐧 𝐝𝐨 𝐭𝐡𝐢𝐬."

    bot.reply_to(message, response)

# Redeem key command
@bot.message_handler(commands=['redeem'])
def redeem_key_command(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        key = command[1]
        if key in keys:
            expiration_date = keys[key]
            users[user_id] = expiration_date
            save_data(users, keys)
            del keys[key]
            save_data(users, keys)
            response = f"✅𝐊𝐞𝐲 𝐫𝐞𝐝𝐞𝐞𝐦𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲! 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝 𝐔𝐧𝐭𝐢𝐥: {expiration_date}"
        else:
            response = "𝐄𝐱𝐩𝐢𝐫𝐞𝐝 𝐊𝐞𝐲 𝐌𝐚𝐭 𝐃𝐚𝐚𝐋 𝐋𝐚𝐰𝐝𝐞."
    else:
        response = "𝐔𝐬𝐚𝐠𝐞: /redeem <key>"

    bot.reply_to(message, response)

# Show all users command
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in map(str, ADMIN_IDS):
        if users:
            response = "𝐂𝐇𝐔𝐓𝐘𝐀 𝐔𝐒𝐑𝐄𝐑 𝐋𝐈𝐒𝐓:\n"
            for user_id, expiration_date in users.items():
                try:
                    user_info = bot.get_chat(int(user_id))
                    username = user_info.username if user_info.username else f"UserID: {user_id}"
                    response += f"- @{username} (ID: {user_id}) expires on {expiration_date}\n"
                except Exception:
                    response += f"- 𝐔𝐬𝐞𝐫 𝐢𝐝: {user_id} 𝐄𝐱𝐩𝐢𝐫𝐞𝐬 𝐨𝐧 {expiration_date}\n"
        else:
            response = "𝐀𝐣𝐢 𝐋𝐚𝐧𝐝 𝐌𝐞𝐫𝐚"
    else:
        response = "𝐁𝐇𝐀𝐆𝐉𝐀 𝐁𝐒𝐃𝐊 𝐎𝐍𝐋𝐘 𝐎𝐖𝐍𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐀𝐓"
    bot.reply_to(message, response)

# Payload command
@bot.message_handler(commands=['payload'])
def payload_command(message):
    user_id = str(message.chat.id)
    if user_id not in users:
        bot.reply_to(message, "𝐘𝐨𝐮 𝐜𝐚𝐧𝐧𝐨𝐭 𝐠𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐚 𝐩𝐚𝐲𝐥𝐨𝐚𝐝 𝐭𝐢𝐥𝐥 𝐲𝐨𝐮 𝐫𝐞𝐝𝐞𝐞𝐦 𝐚 𝐤𝐞𝐲.")
        return
    
    command = message.text.split()
    if len(command) == 2:
        try:
            size_kb = int(command[1])
            payload = generate_payload(size_kb)

            # Split the payload into manageable chunks
            chunk_size = 4096 - len("Generated Payload:\n```\n```\n")  # Adjust for formatting
            chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]
            
            for chunk in chunks:
                bot.reply_to(message, f'Generated Payload:\n```\n{chunk}\n```', parse_mode="Markdown")
                
        except ValueError:
            bot.reply_to(message, "Please provide a valid payload size in KB (e.g., /payload 1).")
    else:
        bot.reply_to(message, "Usage: /payload <size in KB>")



# Function to generate random bytecode-like payload
def generate_payload(size_kb):
    size_bytes = size_kb * 1024
    # Generate random bytes and represent them in a byte-like format
    payload = bytearray(random.getrandbits(8) for _ in range(size_bytes))
    return ''.join(f'\\x{byte:02x}' for byte in payload)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    username = message.from_user.username if message.from_user.username else "N/A"
    user_role = "Admin" if user_id in map(str, ADMIN_IDS) else "User"
    expiration_date = users.get(user_id, "Not Approved")
    response = (f"👤 Your Info:\n\n"
                f"🆔 User ID: <code>{user_id}</code>\n"
                f"📝 Username: {username}\n"
                f"🔖 Role: {user_role}\n"
                f"📅 Approval Expiry Date: {expiration_date}")
    bot.reply_to(message, response, parse_mode="HTML")

# Help command
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''𝐌𝐄𝐑𝐀 𝐋𝐀𝐍𝐃 𝐊𝐀𝐑𝐄 𝐇𝐄𝐋𝐏 𝐓𝐄𝐑𝐈 𝐋𝐄 𝐅𝐈𝐑 𝐁𝐇𝐈 𝐁𝐀𝐓𝐀 𝐃𝐄𝐓𝐀:
💥 /rules: 𝐅𝐨𝐥𝐥𝐨𝐰 𝐞𝐥𝐬𝐞 𝐑𝐚𝐩𝐞.
💥 /redeem <key>: 𝐊𝐞𝐲 𝐑𝐞𝐝𝐞𝐞𝐦 𝐰𝐚𝐥𝐚 𝐂𝐨𝐦𝐦𝐚𝐧𝐝.
💥 /payload <size>: 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐚 𝐩𝐚𝐲𝐥𝐨𝐚𝐝.
💥 /genkey <amount> <hours/days>: 𝐓𝐎 𝐌𝐀𝐊𝐄 𝐊𝐄𝐘.
💥 /allusers: 𝐋𝐢𝐒𝐓 𝐎𝐅 𝐂𝐇𝐔𝐓𝐘𝐀 𝐔𝐒𝐄𝐑𝐒.
💥 /broadcast <message>: 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐊𝐀 𝐌𝐀𝐓𝐋𝐀𝐁 𝐓𝐎 𝐏𝐀𝐓𝐀 𝐇𝐎𝐆𝐀 𝐀𝐍𝐏𝐀𝐃.
'''
    bot.reply_to(message, help_text)

# Broadcast command
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    user_id = str(message.chat.id)
    if user_id in map(str, ADMIN_IDS):
        command = message.text.split(maxsplit=1)
        if len(command) == 2:
            broadcast_message = command[1]
            for user in users.keys():
                try:
                    bot.send_message(user, broadcast_message)
                except Exception as e:
                    print(f"Failed to send message to {user}: {e}")
            bot.reply_to(message, "Broadcast message sent successfully.")
        else:
            bot.reply_to(message, "Usage: /broadcast <message>")
    else:
        bot.reply_to(message, "𝐎𝐧𝐥𝐲 𝐏𝐚𝐩𝐚 𝐎𝐟 𝐛𝐨𝐭 𝐜𝐚𝐧 𝐝𝐨 𝐭𝐡𝐢𝐬.")

# Main loop to run the bot
if __name__ == "__main__":
    bot.polling()
