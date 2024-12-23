import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    # TODO: figure out why this worked exactly once then spits 403 every time since.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open('congress.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        return response.text
    else:
        print(f"Failed.  Status code = {response.status_code}")


def scrape_vote_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the vote number and description
    vote_info = soup.find('div', class_='vote-info')
    vote_number = vote_info.find('span', class_='number').text.strip()
    vote_description = vote_info.find('span', class_='description').text.strip()
    
    # Find the table with voting records
    table = soup.find('table', class_='rollcall-votes')
    if table:
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:  # Skip header
            cols = row.find_all('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                party_state = cols[1].text.strip()
                vote = cols[2].text.strip()
                data.append([name, party_state, vote])
    
        # Write to CSV
        with open('house_voting_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Party-State', 'Vote'])  # Header row
            writer.writerows(data)
        print(f"Vote {vote_number} - {vote_description} data has been written to CSV.")
    

def main():
    congress_url = "https://www.congress.gov/roll-call-votes"
    get_html(congress_url)


if __name__ == '__main__':
    print("Let's go!")
    main()

    print("Done.")