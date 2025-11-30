# Telegram Random Song Bot

<p align="center">
  <img src="assets/preview.png" alt="Bot Preview" width="420">
</p>

A simple Telegram bot built with **Aiogram (v3)** that sends a random `.mp3` or `.mp4` file from a local music folder to a list of authorized users.
Perfect for sharing songs privately with selected people.

---

## Features

* 🎵 Sends a **random song/video** (`.mp3` or `.mp4`) when the user sends `"1"`.
* 🔒 Only authorized users can interact with the bot.
* 📜 Full logging to console + `chat_log.txt`.
* 🔁 Handles Telegram rate limits using `RetryAfter`.
* 🛠 Easy to extend (DB, playlists, remote storage, etc.).

---

## Preview Image

Replace `assets/preview.png` with your actual image path.

```
📌 Place your image here:
assets/preview.png
```

Example structure:

```
your-repo/
 ├── bot.py
 ├── README.md
 ├── assets/
 │    └── preview.png
```

---

## Installation

### 1. Install dependencies

Create a `requirements.txt`:

```
aiogram>=3.0.0
python-dotenv>=1.0.0
```

Install:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```
API_TOKEN=123456:ABC-DEF...
TARGET_USER_IDS=123456,987654321
MUSIC_FOLDER=/path/to/music
```

Add `.env` to `.gitignore` (important!):

```
.env
chat_log.txt
```

---

## Running the bot

```bash
python bot.py
```

---

## Usage

Authorized users:

1. Send `/start`
2. Send `1` → bot responds with a random song/video 🎶
   Unauthorized users receive a warning message.

---

## Troubleshooting

* **Bot blocked by user:** You’ll get `TelegramForbiddenError`.
* **No music files found:** Make sure `.mp3` / `.mp4` files exist in `MUSIC_FOLDER`.
* **Hitting rate limits:** Bot retries automatically after `RetryAfter`.

---

## Project Structure

```
.
├── bot.py
├── README.md
├── chat_log.txt         # auto-generated
├── assets/
│   └── preview.png      # your bot image
└── requirements.txt
```

---

## Contributing

Feel free to submit PRs — improvements are welcome:

* Inline mode
* Playlists
* Cloud-based file storage
* SQLite or Redis integration

---

## License

MIT License.
