# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/utility/application_fuzzer.ipynb.

# %% auto 0
__all__ = ['cache', 'resolve_window_name', 'get_window_names', 'fuzzy_app']

# %% ../../nbs/utility/application_fuzzer.ipynb 1
import win32gui
from collections import OrderedDict
from fuzzywuzzy import process
from typing import List

# %% ../../nbs/utility/application_fuzzer.ipynb 2
def resolve_window_name(approx_name: str, choices: List[str], threshold: int = 85) -> str:
    """
    Resolve an approximate window name to the actual window name.
    
    Parameters:
    approx_name (str): The approximate window name.
    choices (List[str]): A list of possible window names to choose from.
    
    Returns:
    str: The actual window name.
    """
    # Use fuzzy string matching to find the best match for the approximate name.
    match = process.extractOne(approx_name, choices)
    
    if match[1] >= threshold: # Matching score is 90 or higher
        return match[0]
    else: # No good match was found
        return ''

def get_window_names() -> List[str]:
    """
    Get a list of all the window names on the desktop.
    
    Returns:
    List[str]: A list of window names.
    """
    windows = []
    
    def _enum_windows(hwin, _):
        """
        Enumerate the windows and add their names to the list.
        """
        if win32gui.IsWindowVisible(hwin):
            text = win32gui.GetWindowText(hwin)
            if text:
                windows.append(text)
    
    # Enumerate the windows and add their names to the list.
    win32gui.EnumWindows(_enum_windows, 0)
    
    return windows

# Create an ordered dictionary to store the results of previous calls.
# The maximum number of items in the cache is 1000.
cache = OrderedDict(maxlen=10)

def fuzzy_app(approx_name: str) -> str:
    """
    Resolve an approximate window name to the actual window name using magic.
    
    Parameters:
    approx_name (str): The approximate window name.
    
    Returns:
    str: The actual window name.
    """
    # Check if the approximate window name is in the cache.
    if approx_name in cache:
        # Return the result from the cache.
        return cache[approx_name]
    
    # Get a list of all the window names on the desktop.
    choices = get_window_names()
    
    # Resolve the approximate window name to the actual window name.
    actual_name = resolve_window_name(approx_name, choices)
    
    # Add the result to the cache.
    cache[approx_name] = actual_name
    
    if actual_name != '':
        return actual_name
    else:
        raise Exception(f'magic_resolver failed to resolve {approx_name} list of windows is:{choices}')
