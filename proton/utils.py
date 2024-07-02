import shutil, os
from urllib.parse import urlparse
def remove_indentation(text):
    lines = text.split('\n')  # Split the text into lines
    index = 0
    if len(lines) >= 2:
       index = 1 
    if lines:
        first_line_indent = len(lines[index]) - len(lines[index].lstrip())  # Get the amount of indentation in the first line
        modified_lines = [line[first_line_indent:] for line in lines]  # Remove indentation from each line
        result = '\n'.join(modified_lines)  # Join the modified lines back together
        return result
    return text  # Return the original text if it's empty

class Object():
    def __str__(self):
        return f"Object ({self.__dict__})"
    def __repr__(self):
        return f"Object ({self.__dict__})"
    def __dict__(self):
        return self.__dict__

def toObject(dic: dict):
    o = Object()
    o.__dict__ = dic
    return o

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def remove_files(path: str) -> None:
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.remove(path)