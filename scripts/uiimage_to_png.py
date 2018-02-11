"""Converts a UIImage to a .png file. Then opens it in finder.

Note: The file will be saved in the NSDocumentDirectory as "uiimage.png".
      Subsequent calls into this command will overwrite that file, so it is
      recommended that you make a local copy of the file if you wish to keep it
      long term.

Usage: png <UIImage instance>
"""
import lldb
import shlex

from subprocess import call

def uiimage_to_png(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 1:
    result.Print('ERROR: Please enter the command as "png <UIImage instance>".')
    return
  # Ensure we have a UIView instance. If not, return and print an error message.
  uiimage_check_cmd = 'po (BOOL)[' + args[0] + ' isKindOfClass:[UIImage class]]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(uiimage_check_cmd, temp_result)
  if temp_result.GetOutput().strip() == 'NO':
    result.Print('ERROR: This command only works for UIImages. Enter the command as "png <UIImage instance>".')
    return

  cmd = """
    @import UIKit;

    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *basePath = (paths.count > 0) ? paths[0] : nil;

    NSData *binaryImageData = UIImagePNGRepresentation({0});
    NSString *filePath = [basePath stringByAppendingPathComponent:@"uiimage.png"];
    [binaryImageData writeToFile:filePath atomically:YES];
    filePath;  // Return the NSString as the object to access it's value as the description.
  """.format(args[0])
  target = debugger.GetSelectedTarget()
  if target is None:
    result.Print('ERROR: Could not get selected target.')
    return
  ret_value = target.EvaluateExpression(cmd)
  if not ret_value.GetError().Success():
    result.Print(ret_value.GetError())
    return
  png_path = ret_value.GetObjectDescription()
  if png_path is None:
    result.Print('ERROR: UIImage could not be saved.')
    return
  call(['open', png_path])
  result.Print('UIImage saved to:\n' + png_path)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f uiimage_to_png.uiimage_to_png png')
