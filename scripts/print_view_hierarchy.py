"""Prints the current view hierarchy.

Usage: pv
"""
def print_view_hierarchy(debugger, command, result, internal_dict):
  debugger.HandleCommand('po [[UIWindow keyWindow] recursiveDescription]')


def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f print_view_hierarchy.print_view_hierarchy pv')
