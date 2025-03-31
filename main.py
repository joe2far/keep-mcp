"""
A FastMCP server that provides tools for calculating dimensions based on aspect ratios.
This server specifically handles 16:9 aspect ratio calculations.
"""

from mcp.server.fastmcp import FastMCP
from keep_api import get_notes, create_note

mcp = FastMCP("my-mcp-ratio-server")

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """Get all Google Keep notes as a resource"""
    return get_notes()


@mcp.tool()
def get_height_for_16_9(width: float) -> float:
    """
    Get the height value for a given width using 16:9 aspect ratio.
    
    Args:
        width (float): The width value
        
    Returns:
        float: The calculated height value
    """
    return (width * 9) / 16


@mcp.tool()
def create_keep_note(title: str, text: str, pinned: bool = False) -> str:
    """
    Create a new Google Keep note.
    
    Args:
        title (str): The title of the note
        text (str): The content of the note
        pinned (bool, optional): Whether the note should be pinned. Defaults to False.
        
    Returns:
        str: JSON string containing the created note's data
    """
    return create_note(title, text, pinned)


if __name__ == "__main__":
    mcp.run(transport='stdio')