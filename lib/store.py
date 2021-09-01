#!/usr/bin/env python3

from typing import Dict

import json
import requests
import settings


def get_game_by_id(_id: str) -> Dict:
    r = requests.post(settings.STORE_API_URL, data={"productIds": _id})
    d: Dict = r.json()
    return d


def extract_price(d: Dict) -> Dict:
    price: Dict = {}
    try:
        price = d['Products'][0]['DisplaySkuAvailabilities'][0]['Availabilities'][0]['OrderManagementData']['Price']
    except KeyError:
        # print("--> error, see debug.json")
        # with open("debug.json", "w") as f:
            # json.dump(d, f, indent=2)
        raise
    #
    return price


def extract_title(d: Dict) -> str:
    title: str = d['Products'][0]['LocalizedProperties'][0]['ProductTitle']
    return title
