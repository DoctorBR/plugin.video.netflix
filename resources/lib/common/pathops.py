# -*- coding: utf-8 -*-
"""Helper functions for retrieving values from nested dicts"""
from __future__ import unicode_literals


def get_path(path, search_space, include_key=False):
    """Retrieve a value from a nested dict by following the path.
    Throws KeyError if any key along the path does not exist"""
    if not isinstance(path, (tuple, list)):
        path = [path]
    current_value = search_space[path[0]]
    if len(path) == 1:
        return (path[0], current_value) if include_key else current_value
    return get_path(path[1:], current_value, include_key)


def get_path_safe(path, search_space, include_key=False, default=None):
    """Retrieve a value from a nested dict by following the path.
    Returns default if any key in the path does not exist."""
    try:
        return get_path(path, search_space, include_key)
    except KeyError:
        return default


def remove_path(path, search_space, remove_remnants=True):
    """Remove a value from a nested dict by following a path.
    Also removes remaining empty dicts in the hierarchy if remove_remnants
    is True"""
    if not isinstance(path, (tuple, list)):
        path = [path]
    if len(path) == 1:
        del search_space[path[0]]
    else:
        remove_path(path[1:], search_space[path[0]])
        if remove_remnants and not search_space[path[0]]:
            del search_space[path[0]]


def get_multiple_paths(path, search_space, default=None):
    """Retrieve multiple values from a nested dict by following the path.
    The path may branch into multiple paths at any point.
    A branch point is a list of different keys to follow down the path.
    Returns a nested dict structure with nested dicts for each branch point in
    the path. This essentially reduces the original nested dict by removing
    those layers that only have one key and keys not specified in the branch
    point. Keys specified in branch points that do not exist in the search
    space are silently ignored"""
    if not isinstance(search_space, (dict, list)):
        return default
    if isinstance(path[0], list):
        return {k: get_multiple_paths([k] + path[1:], search_space, default)
                for k in path[0]
                if k in search_space}
    current_value = search_space.get(path[0], default)
    return (current_value
            if len(path) == 1
            else get_multiple_paths(path[1:], current_value, default))