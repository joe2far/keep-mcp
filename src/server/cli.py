"""
MCP plugin for Google Keep integration.
Provides tools for interacting with Google Keep notes through MCP.
"""

import json
from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from .keep_api import get_client, serialize_note, can_modify_note

mcp = FastMCP("keep")

@mcp.tool()
def find(query="") -> str:
    """
    Find notes based on a search query.
    
    Args:
        query (str, optional): A string to match against the title and text
        
    Returns:
        str: JSON string containing the matching notes with their id, title, text, pinned status, color and labels
    """
    keep = get_client()
    notes = keep.find(query=query, archived=False, trashed=False)
    
    notes_data = [serialize_note(note) for note in notes]
    return json.dumps(notes_data)

@mcp.tool()
def create_note(title: Optional[str] = None, text: Optional[str] = None, labels: List[str] = None, color Optional[str] = None) -> str:
    """
    Create a new note with title, text, labels and color.
    
    Args:
        title (str, optional): The title of the note
        text (str, optional): The content of the note
        labels (List[str], optional): List of label names to add to set on the note
        color (str, optional): The color of the note, one of "DEFAULT", "RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE", "CERULEAN", "PURPLE", "PINK", "BROWN", "GRAY"
        
    Returns:
        str: JSON string containing the created note's data
    """
    keep = get_client()
    note = keep.createNote(title=title, text=text)
    
    labels.append('keep-mcp')
    for label_name in labels:
        label = keep.findLabel(label_name)
        if not label:
            label = keep.createLabel(label_name)
        note.labels.add(label)

    if color is not None:
        note.color = color
    
    keep.sync()  # Ensure the note is created and labeled on the server
    
    return json.dumps(serialize_note(note))

@mcp.tool()
def update_note(note_id: str, title: Optional[str] = None, text: Optional[str] = None, labels: List[str] = None, color Optional[str] = None)-> str:
    """
    Update a note's properties.
    
    Args:
        note_id (str): The ID of the note to update
        title (str, optional): New title for the note
        text (str, optional): New text content for the note
        labels (List[str], optional): List of label names to add to set on the note
        color (str, optional): The color of the note, one of "DEFAULT", "RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE", "CERULEAN", "PURPLE", "PINK", "BROWN", "GRAY"
        
        
    Returns:
        str: JSON string containing the updated note's data
        
    Raises:
        ValueError: If the note doesn't exist or cannot be modified
    """
    keep = get_client()
    note = keep.get(note_id)
    
    if not note:
        raise ValueError(f"Note with ID {note_id} not found")
    
    if not can_modify_note(note):
        raise ValueError(f"Note with ID {note_id} cannot be modified (missing keep-mcp label and UNSAFE_MODE is not enabled)")
    
    if title is not None:
        note.title = title
    if text is not None:
        note.text = text

    for label_name in labels:
        label = keep.findLabel(label_name)
        if not label:
            label = keep.createLabel(label_name)
        note.labels.add(label)

    if color is not None:
        note.color = color
    
    keep.sync()  # Ensure changes are saved to the server
    return json.dumps(serialize_note(note))

@mcp.tool()
def delete_note(note_id: str) -> str:
    """
    Delete a note (mark for deletion).
    
    Args:
        note_id (str): The ID of the note to delete
        
    Returns:
        str: Success message
        
    Raises:
        ValueError: If the note doesn't exist or cannot be modified
    """
    keep = get_client()
    note = keep.get(note_id)
    
    if not note:
        raise ValueError(f"Note with ID {note_id} not found")
    
    if not can_modify_note(note):
        raise ValueError(f"Note with ID {note_id} cannot be modified (missing keep-mcp label and UNSAFE_MODE is not enabled)")
    
    note.delete()
    keep.sync()  # Ensure deletion is saved to the server
    return json.dumps({"message": f"Note {note_id} marked for deletion"})

def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    
