"""Prints the current view controller hierarchy.

Usage: pvc
"""
def print_view_controller_hierarchy(debugger, command, result, internal_dict):
  debugger.HandleCommand('po [[[UIWindow keyWindow] rootViewController] _printHierarchy]')


def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f print_view_controller_hierarchy.print_view_controller_hierarchy pvc')
