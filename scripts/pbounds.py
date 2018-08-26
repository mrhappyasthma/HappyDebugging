"""Prints the `bounds` of an object as a CGRect.

Usage: pbounds <instance>
"""
import lldb
import shlex

def pbounds(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 1:
    result.Println('ERROR: Please enter the command as "pframe <instance>".')
    return
  responds_to_selector_check_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:@selector(bounds)]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_check_cmd, temp_result)
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: This command only works for objects that respond to the `bounds` selector.')
    return

  cmd = 'po (CGRect)[' + args[0] + ' bounds]'
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f pbounds.pbounds pbounds')
