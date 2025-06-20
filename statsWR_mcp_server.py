import json
import httpx
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("statsWR")

def load_sample_champion(champion_label:str = "AATROX") -> dict[str, Any] | None:
    file_path = 'data/sample_champions.json'

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        if champion_label in data:
            return data[champion_label]
        else:
            return None
    except Exception as e:
        print("An Error has occured:", e)
        return None

# start of MCP endpoints
@mcp.tool()
async def get_champion_data_from_label(champion_label: str) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        champion_label: Capitalized champion full name. 
                        If a champion's name consists of multiple words, connect them using "_".
                        For example: "Aatrox" -> "AATROX", "Master Yi" -> "MASTER_YI".
    """

    data = load_sample_champion(champion_label)

    if data:
        return str(data)
    return ""


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
