from auto_sre.model import OllamaModel
from auto_sre.system_representation import Node, create_description
from auto_sre.build_tree import tree_from_path
from pathlib import Path

# Change this to path to software package on your machine
PROJECT_PATH = Path("/Users/mackenzievanzanden/Projects/pickle_bot/pickle_bot")
MODEL_NAME = "granite-code:8b"
LLM = OllamaModel(MODEL_NAME)

root: Node = tree_from_path(PROJECT_PATH)
project_description = create_description(root, LLM)

print(project_description)
