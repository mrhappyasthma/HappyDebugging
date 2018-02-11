"""Sets the `bounds` of an object.

Usage: setbounds <instance> <x> <y> <width> <height>
"""
import lldb
import shlex

def set_bounds(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 5:
    print 'ERROR: Please enter the command as "setbounds <instance> <x> <y> <width> <height>".'
    return

  responds_to_selector_check_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:@selector(setBounds:)]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_check_cmd, temp_result)
  if temp_result.GetOutput().strip() == 'NO':
    print 'ERROR: This command only works for objects that respond to the `setBounds:` selector.'
    return

  cmd = 'po (void)[' + args[0] + ' setBounds:(CGRect){{ {0}, {1}, {2}, {3} }}]'.format(args[1], args[2], args[3], args[4])
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f set_bounds.set_bounds setbounds')
