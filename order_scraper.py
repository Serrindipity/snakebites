import argparse
from bs4 import BeautifulSoup
import re

def make_parsed_args():
        parser = argparse.ArgumentParser(prog = "Order Scraper", description="Scrapes TCG Player Order numbers and names from confirmation page")
        parser.add_argument('filename')
        parser.add_argument('outfile', default = 'results.md')
        return parser.parse_args()

def main():
    print("running main")
    args = make_parsed_args()
    filepath = args.filename
    outfile_path = args.outfile
    output = []
    find_order_number = "[A-Z0-9]{8}-[A-Z0-9]{6}-[A-Z0-9]{5}"
    find_date = "Estimated delivery:\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s\d{1,2},\s\d{4}\s-\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s\d{1,2},\s\d{4}"
    find_vendor = r"from\s([^.<\n]+)"
    with open(filepath, 'r') as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
        package_number = 0
        for package in soup.find_all(class_=re.compile("Detail")):
            package_number += 1
            vendor = re.search(find_vendor, package.prettify()).group()
            order_number = re.search(find_order_number, package.prettify()).group()
            delivery_string = re.search(find_date, package.prettify()).group()
            package_string = f"- [ ] Package #{package_number}\n\t- {order_number}\n\t- {vendor}\n\t- {delivery_string}"
            output.append(package_string)
    with open(outfile_path, 'w') as outfile:
        outfile.writelines(i + "\n" for i in output)
                                

if __name__ == "__main__":
    main()