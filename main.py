#!/usr/bin/env python3

import re
from pprint import pprint
from typing import Dict, List

from yachalk import chalk

from lib import store

Url = str

INPUT = "gamelist.txt"


class Game:
    def __init__(self, url: Url) -> None:
        self.url = url
        self.id = self._get_id(url)

        # these will be set later:
        self.title = ""
        self.currency = ""
        self.prev_price = 0
        self.now_price = 0

    def _get_id(self, url: Url) -> str:
        return url.split("/")[-1]

    def on_sale(self):
        return self.now_price < self.prev_price
# endclass


def extract_urls(fname: str, must_contain="") -> List[Url]:
    with open(fname) as f:
        lines = [line for line in f.read().splitlines() if not line.lstrip().startswith("#")]
        content = "\n".join(lines)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        return [url for url in urls if must_contain in url]


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", "\xa0")


def main() -> None:
    urls: List[Url] = extract_urls(INPUT, must_contain="www.xbox.com")

    games: List[Game] = [Game(url) for url in urls]
    for game in games:
        d: Dict = store.get_game_by_id(game.id)
        game.title = store.extract_title(d)
        try:
            price: Dict = store.extract_price(d)
        except KeyError:
            template_error = f"""
{game.title if not game.on_sale() else chalk.green.bg_gray.bold(game.title)} [ {game.url} ]
({chalk.red.bold("error")})
{"-" * 20}
""".strip()
            print(template_error, flush=True)
            continue
        # pprint(price)
        game.currency = price['CurrencyCode']
        game.prev_price = int(price['MSRP'])
        game.now_price = int(price['ListPrice'])
        template_ok = f"""
{game.title if not game.on_sale() else chalk.green.bg_gray.bold(game.title)} [ {game.url} ]
(before: {fmt(game.prev_price)} {game.currency}, now: {fmt(game.now_price)} {game.currency})
{"-" * 20}
""".strip()
        print(template_ok, flush=True)
        # break

##############################################################################

if __name__ == "__main__":
    main()
