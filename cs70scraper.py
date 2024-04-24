# Scraper for UC Berkeley's CS 70. Uses hashcat notation
import requests
import re

disc_base = "https://eecs70.org/assets/pdf/dis?2?1-sol.pdf"
charsets = {
    "?1" : ["a","b"],
    "?2" : ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"],
    "?d" : range(10)
}

def parse_url(url):
    charset_symbols = ','.join(i.rsplit('?')[1] for i in charsets.keys()) # Pulls all possible symbols from the charsets
    regex = f"([?]{{1}}[{charset_symbols}]{{1}})" # Regex splits on "?x" symbols
    parsed = [i for i in re.split(regex,url) if i != ''] # Removes empty strings
    return parsed


def generate_permutations(lst):
    def recurse(current_list, index):
        # If we have filled all placeholders, yield this permutation
        if index == len(current_list):
            yield current_list
            return
        
        current_item = current_list[index]
        # Check if the current item is a placeholder
        if current_item in charsets:
            # Iterate over possible replacements
            for replacement in charsets[current_item]:
                # Recurse with the replacement
                yield from recurse(current_list[:index] + [replacement] + current_list[index+1:], index + 1)
        else:
            # If not a placeholder, continue with the next item
            yield from recurse(current_list, index + 1)

    # Start the recursion from the first index
    return list(recurse(lst, 0))

def make__disc_requests(parsed_url):
    urls = generate_permutations(parsed_url)
    for i in urls:
        url_string = ''.join(i)
        req = requests.get(url_string)
        # TD: Download and write requests.content to file
        # TD: Auto push to Git


parsed = parse_url(disc_base)
print(generate_permutations(parsed))
    