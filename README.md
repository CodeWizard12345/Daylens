# DayLens

An ESP32-CAM time-lapse camera that photographs your day, paired with a small Flask server that receives and displays the photos. The goal is a personal tracker: capture a photo every few seconds, send each hour's batch to a website, and review where your time actually went.

> **Status: work in progress.**
> - The firmware compiles. It has **not yet been tested on real hardware** (parts are on order).
> - The Flask server **is tested** (uploads with `curl` and gallery view work).
> - WiFi upload from the ESP32 to the server is **not written yet** (see Roadmap).

## What works today

- **Firmware (`src/main.cpp`):** initialises the AI-Thinker ESP32-CAM, takes a JPEG photo every 10 seconds, and saves it to the microSD card as `photo_N.jpg`.
- **Server (`server/app.py`):** a Flask app with
  - `POST /upload` to receive a JPEG (filename taken from the `X-Filename` header)
  - `GET /` to show a gallery of all received photos
  - `GET /img/<name>` to serve one photo

## Why photos and not video

Recording 24 hours of video on an ESP32-CAM is not realistic: the SD card fills up (VGA MJPEG is over 1 GB per hour), the board overheats, and FAT32 limits file size. A photo every few seconds is enough to see what you were doing, and 24 hours comes to roughly 10k small JPEGs.

## Hardware

- ESP32-CAM (AI-Thinker)
- FTDI USB-to-serial adapter (the board has no USB port)
- microSD card (FAT32, 32 GB or smaller)
- Stable 5V power supply
- Jumper wires

### Wiring for flashing

| FTDI | ESP32-CAM |
|------|-----------|
| 5V   | 5V        |
| GND  | GND       |
| TX   | U0R       |
| RX   | U0T       |

Connect **GPIO0 to GND** while uploading, remove it afterwards, then press reset.

## Setup

### Firmware

1. Install [VS Code](https://code.visualstudio.com/) and the **PlatformIO IDE** extension.
2. Open this folder in VS Code.
3. Click **Build** (the tick icon in the bottom bar) to compile.
4. With the board connected, click **Upload**, then open the Serial Monitor at 115200 baud. You should see `Ready!` and then `Saved /photo_0.jpg` every 10 seconds.

### Server

```bash
pip install flask
python server/app.py
```

Open http://localhost:5000 to see the gallery. Test it without any hardware:

```bash
curl -X POST --data-binary @photo.jpg -H "X-Filename: test1.jpg" http://localhost:5000/upload
```

On Windows PowerShell use `curl.exe` instead of `curl`.

### Upload API

| Item | Value |
|------|-------|
| Endpoint | `POST /upload` |
| Body | raw JPEG bytes |
| Header | `X-Filename: <name>.jpg` (optional; defaults to a timestamp) |
| Response | `ok` |

## Project structure

```
DayLens/
├── platformio.ini
├── src/
│   └── main.cpp        # ESP32-CAM firmware
├── server/
│   └── app.py          # Flask receiver and gallery
└── README.md
```

## Roadmap

- [ ] Test the firmware on real hardware
- [ ] Connect to WiFi and POST each photo to the server
- [ ] Hourly batch upload, with SD buffering and retry if WiFi drops
- [ ] Deep sleep between captures to reduce heat and power use
- [ ] Wiring diagram image
- [ ] A separate analysis website (not part of this repo)

## Privacy

A camera that runs all day is sensitive. Everyone in the house should know it is there, and photos should only go to a server you control, never a third-party cloud. This project sends nothing anywhere except to the server address you configure yourself.

## Credits

Made by CodeWizard12345.
