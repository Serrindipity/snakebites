# Snakebites - small, simple, but powerful python utilities

## Tag Scraper
Command line utility that scrapes the all the text of a specified HTML tag type

Usage:
```bash
python3 tag_scraper.py [-h] (-u URL | -l [LOAD]) [-t TAG] [-s SAVETO]
```

## TCGPlayer Order Scraper
Command line utility that formats your TCG Player order to a markdown checklist with order number, vendor, and estimated delivery

Usage:
```bash
python3 TCGPlayer_order_scraper.py order_confirmation_html_file outfile
```

## VK Keybinds
Simple python script that maps keybinds in a cfg file to virtual keys. Runs in the background, allowing access to windows virtual keys that might not be usable on the current keyboard.

Keybind format is
```
<modifier_key>+key : vk_code
```

You can use  [[ [this table](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)]] to find codes.

For some simple media keys:
```
<alt>+p : 179
<alt>+j : 177
<alt>+k : 176
<ctrl>+<alt>+q : quit
```