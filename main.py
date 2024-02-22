#libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#for fetching url's data
def fetch_html(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print("Error fetching HTML:", e)
        return None

#for extracting table data
def scrape_table_data(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        table_data = []
        for row in table.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            if row_data:
                table_data.append(row_data)
        return table_data
    except AttributeError as e:
        print("Error parsing HTML:", e)
        return None

#for writing to excel, try csv :), drops column view, has nothing on it
def write_to_excel(table_data, output_file):
    if table_data:
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        if 'View' in df.columns:
            df.drop(columns=['View'], inplace=True)
        df.to_excel(output_file, index=False)
        print("Table data has been written to", output_file)
    else:
        print("No table data to write.")

#calls our func
if __name__ == "__main__":
    url = 'https://kmpdc.go.ke/Registers/General_Practitioners.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    html = fetch_html(url, headers)
    if html:
        table_data = scrape_table_data(html)
        write_to_excel(table_data, 'kmpdc_table_data.xlsx')
