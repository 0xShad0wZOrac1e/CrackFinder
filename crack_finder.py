import datetime
import json
import os.path
import time
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import Session

__version__ = "1.0.0"
__prgm_name__ = "CrackFinder: Find Cracks Around Recognized Sites"


class CustomSession(Session):

    def reset_headers(self):
        self.headers.update({})
        return

    def add_header(self, header_name: str, header: str):
        self.headers[header_name] = header
        return

    def remove_header(self, header_name: str):
        del self.headers[header_name]
        return


def fetch_gog_games(session, search_query, results_dict):
    response = session.get(f"https://www.gog-games.to/search/{search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    search_results = soup.find_all("a", attrs={"class": "block"})
    for result in search_results:
        href = result["href"]
        title = result.find("div", attrs={"class": "info"}).find("span", attrs={"class": "title"}).text
        results_dict["gog-games"][title] = "https://www.gog-games.to" + href


def fetch_gload(session, search_query, results_dict):
    response = json.loads(
        session.post("https://gload.to/wp-admin/admin-ajax.php?action=warp_search", data={"s": search_query}).content)
    for result in response["results"]:
        results_dict["gload"][result["title"]] = urlparse(result["url"]).geturl()


def fetch_online_fix(session, search_query, results_dict):
    response = session.post(f"https://online-fix.me/index.php?do=search&subaction=search&story={search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    articles = soup.find_all("div", attrs={"class": "article clr"})
    for article in articles:
        link = article.find("a", attrs={"class": "big-link"})["href"]
        title = article.find("img", attrs={"class": "lazyload"})["alt"]
        results_dict["online-fix"][title] = link


def fetch_ovagames(session, search_query, results_dict):
    response = session.get(f"https://www.ovagames.com/?s={search_query}&x=0&y=0").content
    soup = BeautifulSoup(response, "html.parser")
    posts = soup.find_all("div", attrs={"class": "home-post-wrap"})
    for post in posts:
        link = post.find("a", attrs={"data-wpel-link": "internal"})
        results_dict["ovagames"][link["title"].replace("Permanent Link to ", "")] = link["href"]


def fetch_g4u(session, search_query, results_dict):
    response = session.get(f"https://g4u.to/en/search/?str={search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    content = soup.find("div", attrs={"class": "w3-content w3-center w3-light-grey"})
    links = content.find_all("a")
    for link in links:
        title = link.find("div", attrs={"class": "w3-opacity w3-tiny"}).text
        results_dict["g4u"][title] = "https://g4u.to" + link["href"]


def fetch_rlsbb(session, search_query, results_dict):
    session.headers["Cookie"] = "filters=games,_games_pc,_games_mac-games"
    response = session.get(f"https://search.rlsbb.ru/?s={search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    entries = soup.find_all("h1", attrs={"class": "entry-title"})
    for entry in entries:
        link = entry.find("a", attrs={"rel": "bookmark"})
        if link is not None:
            results_dict["rlsbb"][link.text] = link["href"]
    del session.headers["Cookie"]


def fetch_downloadha(session, search_query, results_dict):
    response = session.get(f"https://www.downloadha.com/?s={search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    entries = soup.find_all("h2", attrs={"class": "entry-title"})
    for entry in entries:
        title = entry.text
        href = entry.find("a", attrs={"rel": "bookmark"})["href"]
        results_dict["downloadha"][title] = href


def fetch_digitalzone(session, search_query, results_dict):
    response = session.get(f"https://god0654.github.io/DigitalZone/").content
    soup = BeautifulSoup(response, "html.parser")
    entries = soup.find_all("div", attrs={"class": "blog-post"})
    for entry in entries:
        h3: str = entry.find("h3").text
        if h3.lower().__contains__(search_query.lower()):
            href = entry.find("a")["href"]
            results_dict["digitalzone"][h3] = "https://god0654.github.io/DigitalZone" + href


def fetch_gamedrive(session, search_query, results_dict):
    response = session.get(f"https://gamedrive.org/?s={search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    entry = soup.find("div", attrs={"class": "row gridlove-posts"})
    entries_image = entry.find_all("div", attrs={"class": "entry-image"})
    for entry_image in entries_image:
        found = entry_image.find("a")
        href = found["href"]
        title = found["title"]
        results_dict["gamedrive"][title] = href


def fetch_steamrip(session, search_query, results_dict):
    response = session.get(f"https://steamrip.com/search/{search_query}").content
    soup = BeautifulSoup(response, "html.parser")
    entries = soup.findAll("a", attrs={"class": "all-over-thumb-link"})
    for entry in entries:
        results_dict["steamrip"][entry.text] = "https://steamrip.com" + entry["href"]


def main():
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f"{__prgm_name__} (Version {__version__})",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Crack name to find."
    )
    parser.add_argument(
        "--sites",
        default="all",
        help="Sites where is located cracks, separate with ','. Default is 'all'."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=2,
        help="Timeout duration between each request in seconds. Default is 2 seconds."
    )

    parser.add_argument(
        "--save",
        type=bool,
        default=False,
        help="Save the result in a file"
    )

    args = parser.parse_args()

    search_query = args.name
    sites = args.sites.split(',')
    timeout = args.timeout

    session = CustomSession()
    session.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0")
    session.add_header("Accept", "*/*")

    results_dict = {
        "gog-games": {},
        "gload": {},
        "online-fix": {},
        "ovagames": {},
        "g4u": {},
        "rlsbb": {},
        "downloadha": {},
        "digitalzone": {},
        "gamedrive": {},
        "steamrip": {}
    }

    site_functions = {
        "gog-games": fetch_gog_games,
        "gload": fetch_gload,
        "online-fix": fetch_online_fix,
        "ovagames": fetch_ovagames,
        "g4u": fetch_g4u,
        "rlsbb": fetch_rlsbb,
        "downloadha": fetch_downloadha,
        "digitalzone": fetch_digitalzone,
        "gamedrive": fetch_gamedrive,
        "steamrip": fetch_steamrip
    }

    if "all" in sites:
        for site, func in site_functions.items():
            func(session, search_query, results_dict)
            if timeout != 0:
                time.sleep(timeout)
    else:
        for site in sites:
            if site in site_functions:
                site_functions[site](session, search_query, results_dict)
                time.sleep(timeout)
            else:
                print(f"Unkown Site: {site}")

    if args.save:
        if not os.path.isdir("./results"):
            os.mkdir(os.path.join("results"))
        with open("./results/" + datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S") + " result.json",
                  mode="w+") as file:
            file.write(json.dumps(results_dict, indent=4, sort_keys=True, ensure_ascii=False))
            file.close()

    for site, cracks in results_dict.items():
        if cracks:
            print(f"------- {site} -------")
            for crack_name, url in cracks.items():
                print(f"{crack_name} -> {url}\n")


if __name__ == "__main__":
    main()
