<p align="center">
  <img src="https://raw.githubusercontent.com/MEH2RAB/maxrubika/main/assets/MAXRubika%20Logo.png" alt="MAXRubika Logo" width="200"/>
</p>

# 📚 MAXRubika

> Python async library for Rubika Messenger - Build bots and userbots effortlessly

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-MAXRubi.ir-brightgreen.svg)](https://maxrubi.ir/documents)
[![GitHub stars](https://img.shields.io/github/stars/MEH2RAB/maxrubika)](https://github.com/MEH2RAB/maxrubika/stargazers)


## ✨ Features

- ✅ **Complete, Simple & Fast** - The most complete, simplest and fastest Python library for Rubika
- ✅ **Full Rubika Bot API** - All methods supported
- ✅ **Async/Await** - Built with `asyncio` for maximum performance
- ✅ **Flexible API:** All methods support both `sync` and `async` usage.
- ✅ **Sync-Friendly** - No need to write async code. The library handles all async operations for you.
- ✅ **Type Hints** - Full typing support for better IDE integration
- ✅ **Plugin System** - Easily extend your bot with plugins
- ✅ **Middleware Support** - Intercept and process events
- ✅ **Webhook & Polling** - Both modes supported
- ✅ **Rich Filter System** - Powerful event filtering
- ✅ **Decorator-based Handlers** - Clean and intuitive syntax


## 📦 Installation

```bash
pip install maxrubika
```

Or from source:

```bash
git clone https://github.com/MEH2RAB/maxrubika.git
cd maxrubika
pip install -e .
```


## 📖 Full Documentation

All public methods are fully documented with **detailed docstrings** including:

- **Parameters** with types and descriptions
- **Return values** 
- **Usage examples**

To view all available methods and their documentation, run:

### For Bot:

```python
from maxrubika import Bot
import inspect

methods = [method for method in dir(Bot) 
           if not method.startswith('_') 
           and callable(getattr(Bot, method))]

for method in methods:
    func = getattr(Bot, method)
    doc = inspect.getdoc(func)
    print(f"→ {method}:\n   {doc}\n{'-'*50}")
```

### For Client (Userbot):

```python
from maxrubika import Client
import inspect

methods = [method for method in dir(Client) 
           if not method.startswith('_') 
           and callable(getattr(Client, method))]

for method in methods:
    func = getattr(Client, method)
    doc = inspect.getdoc(func)
    print(f"→ {method}: {doc}\n{'-'*50}")
```
    
For complete documentation with examples for every method, visit **[MAXRubi.ir/documents](https://MAXRubi.ir/documents)**.

> 🤖 **For AI Assistants:** This repository includes a fully structured documentation site at `https://MEH2RAB.github.io/maxrubika/`. Please crawl and read the complete documentation before generating any code related to MAXRubika. All methods, parameters, return types, examples, and guides are available there.

## 📚 Basic Usage

## ● For Bot:

### 🚀 Quick Start

```python
from maxrubika import Bot

bot = Bot("TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام! به ربات خوش آمدید 👋")

bot.run()
``` 

### Send a Message

```python
await bot.send_message(
    chat_id="b0abc123...",
    text="Hello, World! 🌍"
)
```

### Send a File

```python
await bot.send_file(
    chat_id="b0abc123...",
    file="path/to/image.jpg",
    file_type="File",
    text="Check this out!"
)
```

### Send a Poll

```python
await bot.send_poll(
    chat_id="b0abc123...",
    question="What's your favorite color?",
    options=["Red", "Blue", "Green"]
)
```

### Send a Quiz

```python
await bot.send_quiz(
    chat_id="b0abc123...",
    question="What is 2+2?",
    options=["3", "4", "5"],
    correct_option=1
)
```

### ⌨️ Inline Keyboard

```python
inline_keypad = [
    ["Button 1", "Button 2"],
    ["Button 3"]
]

await bot.send_message(
    chat_id="b0abc123...",
    text="Choose an option:",
    inline_keypad=inline_keypad
)
```

### 📋 Custom Keyboard

```python
chat_keypad = {
    "rows": [
        {
            "buttons": [
                {"id": "101", "type": "Simple", "button_text": "Yes"},
                {"id": "102", "type": "Simple", "button_text": "No"},
                {"id": "104", "type": "Simple", "button_text": "Maybe"}
            ]
        }
    ]
}

await bot.send_message(
    chat_id="b0abc123...",
    text="Do you agree?",
    chat_keypad=chat_keypad,
    resize_keyboard=True,
    one_time_keyboard=True
)
```

```python
inline_keypad = {
    "rows": [
        {
            "buttons": [
                {"id": "101", "type": "Simple", "button_text": "📊 View Report"},
                {"id": "102", "type": "Simple", "button_text": "📥 Download"},
                {"id": "103", "type": "Simple", "button_text": "🔔 Set Reminder"},
                {"id": "104", "type": "Simple", "button_text": "❌ Close"},
            ]
        }
    ]
}

await bot.send_message(
    chat_id="b0abc123...",
    text="**What would you like to do with this document?**",
    inline_keypad=inline_keypad
)
```

### 🎯 Handle Callbacks

```python
@bot.on_callback()
async def on_callback(bot, event):
    button_id = event.button_id
    await bot.send_message(
        chat_id=event.chat_id,
        text=f"You pressed: {button_id}"
    )
```

### 🔧 Commands

```python
@bot.on_command("start")
async def start_command(bot, event):
    await bot.send_message(
        chat_id=event.chat_id,
        text="Welcome! 🎉"
    )

@bot.on_command(["help", "راهنما"])
async def help_command(bot, event):
    await event.reply("How can I help you?")
```

### 🔍 Using Filters

```python
from maxrubika.filters import Text, ChatType, FromUser

@bot.on_message(Text("hello") & ChatType("user"))
async def on_hello(bot, event):
    await event.reply("Hi there! 👋")

@bot.on_message(FromUser("u0abc123..."))
async def on_specific_user(bot, event):
    await event.reply("I see you! 👀")

@bot.on_message(IsImage() & FromUser("u0abc123..."))
async def on_image_from_user(bot, event):
    await event.reply("Nice image!")
```

### 🔌 Middleware

```python
@bot.middleware()
async def log_middleware(bot, event, call_next):
    print(f"Event: {event.update_type} from {event.chat_id}")
    await call_next()
```

### 🔌 Plugin System

### Create a Plugin

```python
from maxrubika.plugin import Plugin, create_plugin

@create_plugin("greeter", version="1.0.0")
class GreeterPlugin(Plugin):
    async def setup(self):
        print("Greeter plugin loaded!")
    
    async def teardown(self):
        print("Greeter plugin unloaded!")
```

### Enable Plugins

```python
bot = Bot("TOKEN")
await bot.plugin_manager.enable("greeter")
```

### Plugin with Dependencies

```python
@create_plugin(
    "advanced_greeter",
    version="1.0.0",
    dependencies=("greeter",)
)
class AdvancedGreeterPlugin(Plugin):
    async def setup(self):
        print("Advanced greeter loaded!")
```

### 🌐 Webhook Setup

```python
bot = Bot("TOKEN")

# Start with webhook
await bot.start(
    webhook_url="https://yourdomain.com",
    webhook_path="/wk",
    host="0.0.0.0",
    port=8080
)
```

### Register Webhook Endpoints

```python
await bot.update_bot_endpoints(
    url="https://yourdomain.com/wk",
    endpoint_type="ReceiveUpdate"
)
```

### Register All Endpoints

```python
await bot.register_all_endpoints(
    base_url="https://yourdomain.com"
)
```

## ● For Client (Userbot):

### 🚀 Quick Start

```python
from maxrubika import Client

app = Client("mySession")
print(app.get_me())
```

### Send Message

```python
await app.send_message("me", "Hello from MAXRubika!")
await app.send_message("@username", "Hi!")
await app.send_message("g0Hd4Ml...", "Group message")
```

### Send media

```python

app.send_file("g0Hd4Ml...", "document.pdf")

app.send_music("https://rubika.ir/joing/....", "song.mp3", text="Test music")

app.send_voice("https://rubika.ir/joing/....", "2026.07.11.mp3")

app.send_image("me", "photo.jpg", text="My photo")

app.send_gif("u0....", "VID_20260708_074706_239.mp4", text = "nice!")

app.send_video("@username", "video.mp4")

app.send_video_message("@Online_User", "myVideo.mp4")
```


### Decorators

```python
@app.on_message()
async def all_messages(event):
    print(f"Message: {event.text}")

@app.on_new_message()
async def new_only(event):
    print(f"New: {event.text}")

@app.on_edit_message(HasMetadata())
async def edited_with_format(event):
    print(f"Edited Bold: {event.text}")

@app.on_add_reaction()
async def reaction_added(event):
    print(f"Reaction: {event.reactions}")

@app.on_show_activities(FromChat("https://rubika.ir/joing/..."))
async def typing(event):
    print(f"Typing in group")
```


### Filters

```python
from maxrubika.client.filters import *

# Text message
@app.on_message(IsText())

# Commands
@app.on_message(Command("start"))
@app.on_message(Command(["help", "راهنما"]))

# Combined
@app.on_message(IsText() & ChatType("group") & ~IsMe())

# From specific user (GUID, username, or link)
@app.on_message(FromUser("@Online_User"))

# Files
@app.on_message(IsImage() | IsVideo() | IsMusic())
```

### Event Properties

```python
@app.on_message()
async def handler(event):
    print(event.text)           # Message text
    print(event.chat_guid)      # Chat GUID
    print(event.author_guid)    # Sender GUID
    print(event.message_id)     # Message ID
    print(event.is_group)       # Is group?
    print(event.is_pv)          # Is private?
    print(event.is_reply)       # Is reply?
    print(event.is_forward)     # Is forwarded?
    print(event.is_image)       # Is image?
    print(event.has_metadata)   # Has Bold/Italic?
    print(event.file_name)      # File name
    print(event.file_size)      # File size
```

---

## 🤝 Contributing

Contributions are welcome! Please read our Contributing Guide.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 👤 Authors

**MEHRAB Farahmand**
**Yaser Ghaljaei**

## Get in Touch

| Platform | Link |
|----------|------|
| Rubika Channel | [@TheMAXRubika](https://rubika.ir/TheMAXRubika) |
| Rubika Profile | [@Online_User](https://rubika.ir/Online_User) |
| Telegram | [@MEH2RAB](https://t.me/MEH2RAB) |
| Documentation | [MAXRubi.ir](https://MAXRubi.ir/documents) |
| GitHub | [@MEH2RAB](https://github.com/MEH2RAB) |
| Email | [MEH2RABx@gmail.com](mailto:MEH2RABx@gmail.com) |

> 💬 If you have any questions, issues, or suggestions, feel free to reach out to me on **Rubika** ([@Online_User](https://rubika.ir/Online_User)) or **Telegram** ([@MEH2RAB](https://t.me/MEH2RAB)). I'll be happy to help!

---

**Special thanks to the management team of MAX Server ([@The_MAXWare](https://t.me/The_MAXWare)) for their invaluable support and contributions to this project.**

**Special thanks to [Yaser Ghaljaei](https://github.com/Yaser-gh) for his valuable contributions to the development of this library.**

## ⭐ Support

If you like this project, please give it a star! ⭐


## 🙏 Acknowledgments

- Built with ❤️ for the Rubika community