import argparse
from bs4 import BeautifulSoup
import re
import json
import sys


def make_parsed_args():
    parser = argparse.ArgumentParser(
        prog="Order Scraper",
        description="Scrapes TCG Player Order numbers and names from confirmation page or processes JSON orders",
    )
    parser.add_argument("filename", nargs="?", help="Input file (HTML or JSON)")
    parser.add_argument(
        "--json", action="store_true", help="Process input as JSON instead of HTML"
    )
    parser.add_argument(
        "--outfile",
        default="results.md",
        help="Output markdown file (default: results.md)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug output for warnings"
    )
    return parser.parse_args()


def read_input_data(filepath):
    """Read input data from file or stdin."""
    if filepath:
        try:
            # Try UTF-8 first, then UTF-16 if that fails
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="utf-16") as f:
                    return f.read()
        except IOError as e:
            print(f"Error reading file {filepath}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        return sys.stdin.read()


def parse_html(filepath):
    """Parse HTML file and extract raw order data."""
    orders = []
    find_order_number = "[A-Z0-9]{8}-[A-Z0-9]{6}-[A-Z0-9]{5}"
    find_date = "Estimated delivery:\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s\d{1,2},\s\d{4}\s-\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s\d{1,2},\s\d{4}"
    find_vendor = r"from\s([^.<\n]+)"

    with open(filepath, "r") as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
        for package in soup.find_all(class_=re.compile("Detail")):
            vendor = re.search(find_vendor, package.prettify()).group()
            order_number = re.search(find_order_number, package.prettify()).group()
            delivery_string = re.search(find_date, package.prettify()).group()
            orders.append(
                {
                    "vendor": vendor,
                    "order_number": order_number,
                    "delivery": delivery_string,
                }
            )

    return orders


def format_html_orders(orders):
    """Format raw HTML order data for output."""
    output = []
    for idx, order in enumerate(orders, 1):
        order_string = f"- [ ] Package #{idx}\n\t- {order['order_number']}\n\t- {order['vendor']}\n\t- {order['delivery']}"
        output.append(order_string)
    return output


def parse_json(data, debug=False):
    """Parse JSON data and extract raw order data."""
    orders = []

    for order in data:
        products = order.get("products", [])

        # Validate that all products have the same party
        parties = set(product.get("party", "Unknown") for product in products)
        if len(parties) > 1:
            if debug:
                parties_list = ", ".join(sorted(parties))
                print(
                    f"Warning: Order {order.get('vendorId', 'Unknown')} has products from multiple parties: {parties_list}",
                    file=sys.stderr,
                )
            party = "Direct"
        else:
            # Get the party (first product's party, or "Unknown" if no products)
            party = products[0].get("party", "Unknown") if products else "Unknown"

        total_price = sum(
            product.get("price", 0) * product.get("quantity", 1) for product in products
        )
        shipping = order.get("shippingAmount", 0)
        tax = order.get("taxAmount", 0)
        total = total_price + shipping + tax

        orders.append(
            {
                "vendor": order.get("vendor", "Unknown"),
                "vendor_id": order.get("vendorId", "Unknown"),
                "ordered_at": order.get("orderedAt", "Unknown date"),
                "shipping_status": order.get("shippingStatus", "unknown"),
                "item_count": len(products),
                "total": total,
                "products": products,
                "party": party,
            }
        )

    return orders


def format_json_orders(orders):
    """Format raw JSON order data for output."""
    output = []
    for idx, order in enumerate(orders, 1):
        order_string = f"- [ ] Order #{idx} ({order['vendor']}) - {order['party']}\n\t- Order ID: {order['vendor_id']}\n\t- Date: {order['ordered_at']}\n\t- Shipping: {order['shipping_status']}\n\t- Items: {order['item_count']}\n\t- Total: ${order['total']:.2f}"
        output.append(order_string)

        # Add products as subitems
        for product in order.get("products", []):
            product_name = product.get("name", "Unknown")
            product_qty = product.get("quantity", 1)
            product_price = product.get("price", 0)
            product_condition = product.get("condition", "Unknown")
            product_set = product.get("setName", "Unknown")
            product_string = f"\t\t- {product_name} (x{product_qty}) - {product_condition} - {product_set} - ${product_price * product_qty:.2f}"
            output.append(product_string)

    return output


def write_output(formatted_lines, outfile_path):
    """Write formatted lines to output file."""
    with open(outfile_path, "w") as outfile:
        outfile.writelines(line + "\n" for line in formatted_lines)


def main():
    """Main function to process HTML or JSON input."""
    args = make_parsed_args()
    filepath = args.filename
    outfile_path = args.outfile
    use_json = args.json
    debug = args.debug

    try:
        if use_json:
            # Process JSON input
            input_data = read_input_data(filepath)
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}", file=sys.stderr)
                sys.exit(1)

            if not isinstance(data, list):
                print("Error: JSON must be an array of orders", file=sys.stderr)
                sys.exit(1)

            orders = parse_json(data, debug=debug)
            formatted_output = format_json_orders(orders)
        else:
            # Process HTML input (default)
            if not filepath:
                print(
                    "Error: filename is required for HTML processing", file=sys.stderr
                )
                sys.exit(1)
            orders = parse_html(filepath)
            formatted_output = format_html_orders(orders)

        # Write output to file
        write_output(formatted_output, outfile_path)

        print(
            f"Successfully processed {len(formatted_output)} orders and wrote to {outfile_path}"
        )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
