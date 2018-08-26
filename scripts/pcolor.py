import lldb
import shlex


def pcolor(debugger, command, result, internal_dict):
  """Pretty prints a `UIColor` instance as a hex color and RGBA value.

  Usage:
    pcolor <UIColor_instance>
  """
  args = command

  is_kind_of_class_check_cmd = 'po (BOOL)[' + args + ' isKindOfClass:[UIColor class]]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(is_kind_of_class_check_cmd, temp_result)
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: Please enter the command as "pcolor <UIColor_instance>".')
    return

  cmd = """
    @import UIKit;

    CGFloat red, green, blue, alpha;
    [{0} getRed:&red green:&green blue:&blue alpha:&alpha];

    // Convert to 8-bit RGB values.
    red *= 255.0;
    green *= 255.0;
    blue *= 255.0;

    // Create hex string.
    NSString *hexString = [NSString stringWithFormat:@"#%02x%02x%02x",
                           (int)red, (int)green, (int)blue];

    NSString *output = [NSString stringWithFormat:@"RGBA = %d, %d, %d, %.4f\\nHex = %@",
                        (int)red, (int)green, (int)blue, alpha, hexString];
    output;  // Return the NSString as the object to return from the debugger command.
  """.format(args)
#  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

  target = debugger.GetSelectedTarget()
  if target is None:
    result.Println('ERROR: Could not get selected target. Make sure debugger is attached.')
    return
  ret_value = target.EvaluateExpression(cmd)
  if not ret_value.GetError().Success():
    result.Println('"{0}"'.format(ret_value.GetError()))
    return
  output = ret_value.GetObjectDescription()
  if output is None:
    result.Println('ERROR: Could not extract RGBA values for instance: "{0}"'.format(args))
    return
  result.Println(output)

def __lldb_init_module(debugger, internal_dict):
  cmd = ('command script add '
         '-f pcolor.pcolor pcolor '
         '-h "Pretty prints a UIColor instance as a hex color and RGBA value."')
  debugger.HandleCommand(cmd)
