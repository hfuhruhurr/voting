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


def get_html_from_file():
    with open('roll-call-votes.html', 'r') as f:
        html = f.read()
        return BeautifulSoup(html, 'html.parser')

def get_sessions_soup(chamber_soup):
    return chamber_soup.select('ul.plain.list-w-multiple-links > li')    


def get_congresses(sessions):
    congresses = []
    for session in sessions:
        congress_number = session.find('span', class_ = 'title').find('strong').text
        # print(congress_number)

        sessionn_links = session.select('ul > li > a')
        urls = [link['href'] for link in sessionn_links]
        # print(urls)

        congresses.append({
            'congress_number': congress_number,
            'urls': urls,
        })

    return congresses


def get_session_links(html):
    chambers_soup = html.find_all('div', class_ = 'column-equal')

    links = []
    for chamber_soup in chambers_soup:
        chamber = chamber_soup.h2.text
        # print(f"Chamber: {chamber}")
        sessions_soup = get_sessions_soup(chamber_soup)
        congresses = get_congresses(sessions_soup)
        # print(congresses)
        links.append({
            'chamber': chamber,
            'congresses': congresses
        })

    return links


def print_links(session_links):
    for link in session_links:
        print(f"{link['chamber']}:")
        for congress in link['congresses']:
            print(f"    {congress['congress_number']} Congress:")
            for url in congress['urls']:
                print(f"        {url}")    

def main():
    # congress_url = "https://www.congress.gov/roll-call-votes"
    # html = get_html(congress_url)
    html = get_html_from_file()

    session_links = get_session_links(html)
    print_links(session_links)
    

if __name__ == '__main__':
    print("Let's go!")
    main()

    print("Done.")