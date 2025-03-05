"""Create a tree to represent a software package, represented by the `Node` class defined in `system_representation.py`"""
from .system_representation import Node
from pathlib import Path

FILES_TO_IGNORE = ["__pycache__"]
def tree_from_path(path_to_project_root: Path, length_of_root: int = None):
    if length_of_root is None:
        length_of_root = len(path_to_project_root.parts)
    relative_path = Path(*path_to_project_root.parts[length_of_root-1:])
    

    if not path_to_project_root.is_dir():
        root = Node(path=relative_path, value=path_to_project_root.read_text(), children=list())
        return root
    else:
        root = Node(path=relative_path, value=None, children=list())
    
    children = []
    for child_path in path_to_project_root.glob("*"):
        if child_path.name in FILES_TO_IGNORE: continue
        children.append(tree_from_path(child_path, length_of_root))
    
    root.children = children
    return root
        

