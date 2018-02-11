"""Prints the `frame` of an object as a CGRect.

Usage: pframe <instance>
"""
import lldb
import shlex

def pframe(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 1:
    print 'ERROR: Please enter the command as "pframe <instance>".'
    return
  responds_to_selector_check_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:@selector(frame)]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_check_cmd, temp_result)
  if temp_result.GetOutput().strip() == 'NO':
    print 'ERROR: This command only works for objects that respond to the `frame` selector.'
    return

  cmd = 'po (CGRect)[' + args[0] + ' frame]'
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f pframe.pframe pframe')