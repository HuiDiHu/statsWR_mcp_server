import json
import httpx
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

from requests.champion import *

# Initialize FastMCP server
mcp = FastMCP("statsWR")

# start of MCP endpoints
@mcp.tool()
async def get_champion_data_from_label(champion_label: str) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        champion_label: Capitalized champion full name. 
                        If a champion's name consists of multiple words, connect them using "_".
                        For example: "Aatrox" -> "AATROX", "Master Yi" -> "MASTER_YI".
    
    Return:
        A stringified list of dictionaries will be returned. Each dictionary represent a champion's
        gameplay data history for a specific role (indicated by the "role" field). Each number corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
    """

    data = await get_all_data_for_single_champ_all_roles(champion_label)

    if data:
        return str(data)
    return ""


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
