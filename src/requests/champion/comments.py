import httpx
from typing import Any
from mcp_configs import config

async def get_comments_for_one_champ(champion_label:str) -> list[dict[str, Any]] | None:
    url = ""
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=60)
            response.raise_for_status()
        except Exception as e:
            return None

async def get_comments_for_all_champs() -> list[dict[str, Any]] | None:
    url = ""
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=60)
            response.raise_for_status()
        except Exception as e:
            return None