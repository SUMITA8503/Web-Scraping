import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime

# Create a log file to store the scraper's output
log_file = "scraper_log.txt"

def scrape_data():
    Product_name = []
    Prices = []

    url = "https://www.flipkart.com/search?q=mobiles%20phone%20under%2050000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    try:
        # Send a GET request to the URL
        r = requests.get(url)
        r.raise_for_status()  # Raise an exception for bad status codes
        print(f"Request status: {r}")

        # Parse the HTML content
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.prettify()) 

        # Find the container for product information
        box = soup.find("div", class_="DOjaWF gdgoEp")
        
        if box:
            # Extract product names
            names = box.find_all("div", class_="KzDlHZ")
            if not names:
                print("No product names found. Skipping...")
            else:
                for item in names:
                    Product_name.append(item.text.strip())

            # Extract prices
            prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
            if not prices:
                print("No prices found. Skipping...")
            else:
                for item in prices:
                    Prices.append(item.text.strip())

            if len(Product_name) != len(Prices):
                print("Product names and prices do not match. Skipping...")
            else:
                # Create a DataFrame
                df = pd.DataFrame({"Product Name": Product_name, "Prices": Prices})
                # Save the DataFrame to a CSV file
                if os.path.exists("web_scrap_data.csv"):
                    print("Data already saved to CSV.")
                else:
                    # Save to CSV
                    df.to_csv("web_scrap_data.csv", index=False)
                    print("Data successfully saved to CSV.")
        else:
            print("Could not find the product container. The website structure might have changed.")

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Log the scraper's output
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()}: Scraper ran successfully.\n")

if __name__ == "__main__":
    scrape_data()