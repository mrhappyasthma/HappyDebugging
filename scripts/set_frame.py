"""Sets the `frame` of an object.

Usage: setframe <instance> <x> <y> <width> <height>
"""
import lldb
import shlex

def set_frame(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 5:
    print 'ERROR: Please enter the command as "setframe <instance> <x> <y> <width> <height>".'
    return

  responds_to_selector_check_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:@selector(setFrame:)]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_check_cmd, temp_result)
  if temp_result.GetOutput().strip() == 'NO':
    print 'ERROR: This command only works for objects that respond to the `setFrame:` selector.'
    return

  cmd = 'po (void)[' + args[0] + ' setFrame:(CGRect){{ {0}, {1}, {2}, {3} }}]'.format(args[1], args[2], args[3], args[4])
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f set_frame.set_frame setframe')
