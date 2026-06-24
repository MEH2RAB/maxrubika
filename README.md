# 🤖 MAXRubika

> Python async library for Rubika Messenger - Build bots and userbots effortlessly

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-maxrubi.ir-brightgreen.svg)](https://maxrubi.ir)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/maxrubika)](https://github.com/yourusername/maxrubika/stargazers)


## ✨ Features

- ✅ **Full Rubika Bot API** - All methods supported
- ✅ **Async/Await** - Built with `asyncio` for maximum performance
- ✅ **Type Hints** - Full typing support for better IDE integration
- ✅ **Plugin System** - Easily extend your bot with plugins
- ✅ **Middleware Support** - Intercept and process events
- ✅ **Webhook & Polling** - Both modes supported
- ✅ **Rich Filter System** - Powerful event filtering
- ✅ **Decorator-based Handlers** - Clean and intuitive syntax
- ✅ **Zero Dependencies** - Only `aiohttp` required
- 🚧 **UserBot Support** - Coming soon! (Personal account automation)


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


## 🚀 Quick Start

```python
from maxrubika import Bot

bot = Bot("TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام! به ربات خوش آمدید 👋")

bot.run()
```


## 📚 Basic Usage

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

### Send a Photo

```python
await bot.send_image(
    chat_id="b0abc123...",
    image="photo.jpg",
    text="Nice photo!"
)
```

### Send a Video

```python
await bot.send_video(
    chat_id="b0abc123...",
    video="video.mp4",
    text="Watch this!"
)
```

### Send a Voice Message

```python
await bot.send_voice(
    chat_id="b0abc123...",
    voice="voice.mp3",
    text="Listen to this!"
)
```

### Send a Music File

```python
await bot.send_music(
    chat_id="b0abc123...",
    music="song.mp3",
    text="Enjoy the music!"
)
```

### Send a GIF

```python
await bot.send_gif(
    chat_id="b0abc123...",
    gif="animation.gif",
    text="Funny GIF!"
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

### Send a Location

```python
await bot.send_location(
    chat_id="b0abc123...",
    latitude=35.6892,
    longitude=51.3890
)
```

### Send a Contact

```python
await bot.send_contact(
    chat_id="b0abc123...",
    phone_number="+989123456789",
    first_name="MEHRAB",
    last_name="Farahmand"
)
```


## ⌨️ Inline Keyboard

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


## 📋 Custom Keyboard

```python
chat_keypad = [
    ["Yes", "No"],
    ["Maybe"]
]

await bot.send_message(
    chat_id="b0abc123...",
    text="Do you agree?",
    chat_keypad=chat_keypad,
    resize_keyboard=True,
    one_time_keyboard=True
)
```


## 🎯 Handle Callbacks

```python
@bot.on_callback()
async def on_callback(bot, event):
    button_id = event.button_id
    await bot.send_message(
        chat_id=event.chat_id,
        text=f"You pressed: {button_id}"
    )
```


## 🔧 Commands

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


## 🔍 Using Filters

```python
from maxrubika.filters import Text, ChatType, FromUser

@bot.on_new_message(Text("hello") & ChatType("user"))
async def on_hello(bot, event):
    await event.reply("Hi there! 👋")

@bot.on_new_message(FromUser("u0abc123..."))
async def on_specific_user(bot, event):
    await event.reply("I see you! 👀")

@bot.on_new_message(IsImage() & FromUser("u0abc123..."))
async def on_image_from_user(bot, event):
    await event.reply("Nice image!")
```


## 🔌 Middleware

```python
@bot.middleware()
async def log_middleware(bot, event, call_next):
    print(f"Event: {event.update_type} from {event.chat_id}")
    await call_next()
```


## 🔌 Plugin System

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


## 🌐 Webhook Setup

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


## 🔜 Coming Soon: UserBot

```python
from maxrubika import Client
client = Client("mySession")

a = client.get_me()
print(a)
```


## 📁 Project Structure

```
maxrubika/
├── TheBot.py                 # Main Bot class
├── TheClient.py             # UserBot class (coming soon)
├── bot/                   # All Bot modules (unified)
│   ├── __init__.py
│   ├── registry.py        # Handler registry
│   ├── bridge.py          # Bridge between MTProto and Bot API
│   ├── lifecycle.py       # Bot lifecycle management
│   ├── message.py         # Message handling
│   ├── callback.py        # Callback query handling
│   ├── command.py         # Command handling
│   ├── middleware.py      # Middleware system
│   ├── start.py           # Start logic
│   ├── run.py             # Running the bot
│   ├── plugin.py          # Plugin system
│   ├── exceptions.py      # Error classes
│   ├── filters.py         # Event filters
│   ├── metadata.py        # Metadata handling
│   ├── keypad_mixin.py    # Keypad utilities
│   ├── file_extensions.py # File type mappings
│   ├── send_message.py    # Send message methods
│   ├── send_file.py
│   ├── send_poll.py
│   ├── send_quiz.py
│   ├── send_location.py
│   ├── send_contact.py
│   ├── send_image.py
│   ├── send_video.py
│   └── ......
├── types/                 # Type definitions
│   ├── __init__.py
│   ├── incoming.py
│   └── update.py        # Coming soon
├── hybrid.py              # Compatibility layer
└── __init__.py            # Package entry point
```


## 🤝 Contributing

Contributions are welcome! Please read our Contributing Guide.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 👤 Author

**MEHRAB Farahmand**

- Channel: [https://rubika.ir/MAXRubika](https://rubika.ir/MAXRubika)
- Documentation: [https://MAXRubi.ir](https://MAXRubi.ir)
- GitHub: [@MEHRAB](https://github.com/MEH2RAB)


## ⭐ Support

If you like this project, please give it a star! ⭐


## 🙏 Acknowledgments

- Built with ❤️ for the Rubika community