"""Represent a software package as described in the README using an LLM"""
from __future__ import annotations # for recursive node type hint
from .model import Model
from dataclasses import dataclass


@dataclass
class Node:
    """Represents a dir or file in a repository"""
    # Path should be relative to project home 
    path: str
    value: str
    children: list[Node]

    def __eq__(self, other: Node):
        return self.path == other.path

@dataclass
class SoftwareDescription:
    # path of file or directory
    file_name: str
    description: str

def create_prompt(prompt_str: str, **inputs: dict[str, str]) -> str:
    """
        For the following inputs to the fn:
        prompt_str = “Repeat these inputs: {input1}, {input2}”, a = “hello”, b = “there”
        
        We have:
        create_prompt(prompt_str, a, b) == “Repeat these inputs: hello, there”
    """
    return prompt_str.format(**inputs)

def get_output(model: Model, input: str) -> str:
    """ Calls model on ‘input’, returning the output tokens as a single string """
    return model.generate(input)

def _fmt_child_descriptions(child_descriptions: list[SoftwareDescription]):
    return "\n\n".join(
        [f"name: {desc.file_name}\ndescription: {desc.description}" for desc in child_descriptions]
    )

PACKKAGE_DESCRIPTION_SYSTEM_PROMPT = """
You are a software engineering reading the source code of a software package. You will read files or the descriptions of files in some subfolder of the software package,
and either describe the function of the file if given a file as input, or if you are given the descriptions of files in a subfolder, you will use the descriptions of the files to
determine the function of the subfolder.
"""
CREATE_SINGLE_FILE_DESC_PROMPT = """
Here is a code file contained in the software package you aim to describe. You should read the code in the file and output a description of the function of the file.
The description should describe the function of the file. 

Name: {file_name}
Content:
{file_content}
"""
CREATE_SUBTREE_DESC_FROM_CHILD_DESC_PROMPT = """
Here is a list of descriptions of files within a subfolder within the software package you aim to describe. Using the descriptions of the files in the subfolder, you should output
a description of the functionality of the subfolder.

{descriptions}
"""
def create_description(root: Node, llm: Model, depth: int = 0):
    if depth == 0:
        llm.set_system_prompt(PACKKAGE_DESCRIPTION_SYSTEM_PROMPT)

    if not root.children:
        input = create_prompt(CREATE_SINGLE_FILE_DESC_PROMPT, file_name=root.path, file_content=root.value)
        return get_output(llm, input)
    
    child_descriptions = []
    for child in root.children:
        child_description = create_description(child, llm)
        child_descriptions.append(
            SoftwareDescription(
                child.path,
                child_description
            )
        )

    formatted_descriptions = _fmt_child_descriptions(child_descriptions)
    input = create_prompt(CREATE_SUBTREE_DESC_FROM_CHILD_DESC_PROMPT, descriptions=formatted_descriptions)

    # return llm to original state
    if depth == 0:
        # reset llm
        # TODO: Take orig sys prompt to replace, or use to determine if the llm did not originally have a sys prompt
        pass
        
    return get_output(llm, input)
        
    