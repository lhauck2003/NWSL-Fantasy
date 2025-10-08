from bs4 import BeautifulSoup as BS
import cloudscraper
import time, random
import requests
import pandas as pd
import re
from time import sleep

URL = "https://fbref.com/en/comps/182/schedule/NWSL-Scores-and-Fixtures"

BASE_URL = "https://fbref.com"

CSV = "~/NWSL-Fantasy/app/data/player_match_stats.csv"
CSV_test = "nwsl_2025_matches_test.csv"

LINKS_CSV = "match_links.csv"

HEAEDERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}


MAP = {
    "stat_name":"new_stat_name"
}

MONTHS = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

def polite_delay():
    time.sleep(random.uniform(1.0, 2.5))

def make_player_id(team_id, shirt_num):
    return f"{team_id}_{shirt_num}"

def scrape_matches():
    urls = get_match_urls()
    print(f"Found {len(urls)} new match URLs to scrape.")
    for url in urls: 
        scrape_match_to_csv(url, CSV)
        polite_delay()

def scrape_match_to_csv(url, csv_file):
    print(f"Scraping match data from {url}")
    scraper = cloudscraper.create_scraper()  # creates a session that handles Cloudflare
    res = scraper.get(url, headers=HEAEDERS)
    res.raise_for_status()

    soup = BS(res.text, "html.parser")

    all_player_stats = []

    player_stat_table = soup.find_all("div", {"id": re.compile(r"switcher_player_stats_*")})
    

    for table in player_stat_table:
        stats = scrape_player_stats(table, url)
        all_player_stats.extend(stats)


    print(f"Found {len(player_stat_table)} player tables")

    # scrape data into csvc
    df = pd.DataFrame(all_player_stats)
    df.rename(columns=MAP, inplace=True)
    df.to_csv(csv_file, mode='a', header=not pd.io.common.file_exists(csv_file), index=False)

    # print(player_stat_table[0:5])

def scrape_player_stats(table, match_url):
    all_stats = []
    rows = table.find("tbody").find_all("tr", recursive=False)
    team_id = table.get("id", "None")
    team_id = team_id.replace("switcher_player_stats_", "")

    for row in rows:
        player_link = row.find("th", {"data-stat": "player"})
        if not player_link:
            continue

        player_name = player_link.text.strip()
        player_url = BASE_URL + player_link.a["href"] if player_link.a else None

        stats = {"player": player_name, "team_id": team_id, "match_date": MONTHS[match_url.split("/")[-1].split("-")[-4]] + match_url.split("/")[-1].split("-")[-3] + match_url.split("/")[-1].split("-")[-2]}
        for td in row.find_all("td"):
            col = td.get("data-stat")
            val = td.text.strip()
            stats[col] = val
        stats["player_id"] = make_player_id(team_id, stats.get("shirtnumber", "unknown"))
        all_stats.append(stats)
    return all_stats

## Gets all match report URLs from the FBRF schedule page, returns ones not already in the CSV
def get_match_urls():
    scraper = cloudscraper.create_scraper()  # creates a session that handles Cloudflare

    res = scraper.get(URL, headers=HEAEDERS)
    res.raise_for_status()

    soup = BS(res.text, "html.parser")

    match_report_cells = soup.find_all("td", {"data-stat": "match_report"})
    links = [
        BASE_URL + a["href"]
        for cell in match_report_cells
        if (a := cell.find("a")) and a.get("href")
    ]
    # Print them    
    for link in links:
        print(link)

    ## if there is stuff in the CSV, append to it, or else make a new one
    try:
        existing_links = pd.read_csv(LINKS_CSV)["match_url"].tolist()
        links = list(set(links) - set(existing_links))
        pd.DataFrame(links, columns=["match_url"]).to_csv(LINKS_CSV, mode='a', header=False, index=False)
    except: # file does not exist, so make it and read to it
        pd.DataFrame(links, columns=["match_url"]).to_csv(LINKS_CSV, index=False)
    
    
    return links # returns just the links not in the CSV


if __name__ == "__main__":
    scrape_matches()