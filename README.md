# Snakebites - small, simple, but powerful python utilities

## Tag Scraper
Command line utility that scrapes the all the text of a specified HTML tag type

Usage:
```bash
python3 tag_scraper.py [-h] (-u URL | -l [LOAD]) [-t TAG] [-s SAVETO] [-e {HEADER}]
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

You can use [this table](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes) to find codes.

For some simple media keys:
```
<alt>+p : 179
<alt>+j : 177
<alt>+k : 176
<ctrl>+<alt>+q : quit
```

## Seed Finder
A tool for the roguelike NOITA that allows searching through a sessions folder for world seeds based on search parameters.
```bash
python3 seed_finder.py [-h] -f FOLDER [-l LIMIT] [-s SEARCH]
```
Possible search queries include
- items
- heart_containers
- gold_all
- places_visited
- projectiles_shot

> [!NOTE]
> "heart_containers" and "hp" search fields seem to not be working, as every tested file had a measure of 0.