# Simple Command Line Tag Scraper using requests, argparse, and Beautiful Soup 4

#TD: Prettify text that gets returned (strip newlines)
#TD: parse multiple kinds of tags?

import requests
import argparse
from bs4 import BeautifulSoup

default_save = "bypass_save.html"

# Makes the args parser. --url and --load are mutually exclusive, and at least 1 is required.
def make_parsed_args():
        parser = argparse.ArgumentParser(prog = "Tag Scraper", description="Scrapes all tags of a certain type from a given url")
        exclusive = parser.add_mutually_exclusive_group(required=True)
        exclusive.add_argument('-u','--url', type=str, help="url to parse")
        exclusive.add_argument("-l", "--load", nargs = "?", const = default_save, help = f"Loads a file instead of making a request. Overrides all other arguments except --tag.")
        
        parser.add_argument("-t", "--tag", type=str, help = "tag to scrape, if not specified, it just grabs text.")
        parser.add_argument("-s", "--saveto", help = f"filepath to save HTML document to. If unspecified, saves to '{default_save}'")
        
        return parser.parse_args()

# Saves data to a given file
def save_to_file(savedata, filepath = default_save):
    if filepath == None:
        filepath = default_save
    with open(filepath, 'w') as savefile:
        savefile.write(savedata)
    print(f"data saved to {savedata}")


def parse_html(html, tag = None):
    soup = BeautifulSoup(html, 'html.parser')
    if tag:
        tags = soup.find_all(tag)
        text_list = [i.get_text(" ", strip = True) for i in tags]
        print(" ".join(text_list))
    else:
        print(soup.get_text())


def main():
    args = make_parsed_args()
    url = args.url
    tag_to_scrape = args.tag
    #print("Load file is " + str(args.load))

    # Loads the html if no argument is specified
    if args.load:
        html = ""
        try:
            with open(args.load, mode = 'r') as savefile:
                html = savefile.read()
        except:
            print("Error when loading file")
        else:
            parse_html(html, tag_to_scrape)
    # Else makes the get request
    else:
        try:
            print("Making request")
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            response.raise_for_status()
        except:
            print("Something went wrong when making a request.")
            print(f"Status code: {response.status_code}")
        else:
            print(response.text)
            parse_html(response.text, tag_to_scrape)
if __name__ == "__main__":
    main()