from typing import Dict
import re

TAB_REPLACEMENT = ' ' * 4


def standardize_input(in_str: str) -> str:
    """
    Takes in a string, and filters out empty lines and replaces tabs with spaces
    """
    out = []

    for line in in_str.split('\n'):
        line = line.rstrip()

        # Filter out empty lines
        if not line:
            continue

        # Convert tabs to spaces
        line = line.replace('\t', TAB_REPLACEMENT)
        out.append(line)

    out.append('')
    return '\n'.join(out)


def parse_functions(input_program: str) -> Dict[str, Dict[str, str]]:
    """
    Takes in a string with NO BLANK LINES representing the program code, and divides it into functions
    :return: A dictionary of functions, mapped from their name to their attributes
    """
    functions = {}

    # Matches a single function
    multiline_funcs = re.finditer(r'def (\w+)\((.*?)\).*?:\n((?:(?:[ ]{4}|\t).*\n?)*)', input_program)
    oneline_funcs = re.finditer(r'def (\w+)\((.*?)\).*?: ?(.+)', input_program)

    for func_type in [multiline_funcs, oneline_funcs]:
        for func in func_type:
            name = func.group(1)
            arguments = func.group(2)
            if arguments:
                arguments = [arg.strip() for arg in arguments.split(',')]
            else:
                arguments = []

            function_code = func.group(3)
            functions[name] = {"args": arguments, "code": function_code}
    return functions


def parse_imports(input_program: str) -> Dict[str, Dict[str, str]]:
    """
    Takes in a string representing the program code, and parses out the imports (no aliases allowed)
    :return: A dictionary of imports, mapped from the name to a dict of attributes
    """
    pattern = r'(?:^|\n)(?:from|import) (\w*)(?: import )?(.*)'
    python_imports = {}

    # Iterate over all the imports
    for match in re.finditer(pattern, input_program):
        # If we imported a specific function, here it is
        func = match.group(2)
        import_str = match.group(0).strip()
        module_name = match.group(1)

        # If there isn't any specific function, just import the module
        if not func:
            python_imports[match.group(1)] = {"import": import_str, "module": module_name}
        else:
            for f in func.split(','):
                python_imports[f] = {"import": import_str, "module": module_name}

    return python_imports
