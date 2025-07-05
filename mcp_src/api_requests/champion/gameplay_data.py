# make request to statsWR champion gameplay data api

import httpx
from typing import Any
from mcp_src.mcp_configs import config

async def get_all_data_for_single_champ_all_roles(champion_label:str) -> list[dict[str, Any]] | None:
    url = f"{config.API_CONFIG.BASE_URL}/champions/{champion_label}" # first part of path is from vercel deployment, everything afer /v1 is for statsWR route

    print("base url:", config.API_CONFIG.BASE_URL)
    print("default timeout:", config.API_CONFIG.DEFAULT_TIMEOUT)
    print("default headers:", config.API_CONFIG.DEFAULT_HEADERS)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=int(config.API_CONFIG.DEFAULT_TIMEOUT), headers=config.API_CONFIG.DEFAULT_HEADERS)
            response.raise_for_status()
            res = response.json()

            if 'champion' in res.keys():
                return res['champion']

            return None
        except Exception as e:
            print(e)
            return None


async def get_most_recent_data_for_all_champs_by_role(role:int = 0) -> list[dict[str, Any]] | None:
    url = f"{config.API_CONFIG.BASE_URL}/champions/lanes/{role}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=config.API_CONFIG.DEFAULT_TIMEOUT, headers=config.API_CONFIG.DEFAULT_HEADERS)
            response.raise_for_status()
            res = response.json()

            if 'champions' in res.keys():
                return res['champions']

            return None
        except Exception as e:
            print(e)
            return None

__all__ = [
    "get_all_data_for_single_champ_all_roles",
    "get_most_recent_data_for_all_champs_by_role"
]
