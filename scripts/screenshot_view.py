"""Screenshots a UIView and saves it as a .png file. Then opens it in finder.

Note: The file will be saved in the NSDocumentDirectory as "screenshot_view.png".
      Subsequent calls into this command will overwrite that file, so it is
      recommended that you make a local copy of the file if you wish to keep it
      long term.

Usage: screenshot <UIView instance>
"""
import lldb
import shlex

from subprocess import call

def screenshot_view(debugger, command, result, internal_dict):
  args = shlex.split(command)
  if len(args) != 1:
    result.Println('ERROR: Please enter the command as "screenshot <UIView instance>".')
    return
  # Ensure we have a UIView instance. If not, return and print an error message.
  uiview_check_cmd = 'po (BOOL)[' + args[0] + ' isKindOfClass:[UIView class]]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(uiview_check_cmd, temp_result)
  if temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: This command only works for UIViews. Enter the command as "screenshot <UIView instance>".')
    return

  cmd = """
    @import UIKit;

    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *basePath = (paths.count > 0) ? paths[0] : nil;

    CGRect bounds = (CGRect)[{0} bounds];
    UIGraphicsBeginImageContextWithOptions(bounds.size, NO, [UIScreen mainScreen].scale);

    [((UIView *){0}) drawViewHierarchyInRect:bounds afterScreenUpdates:YES];

    UIImage *imageToSave = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();

    NSData *binaryImageData = UIImagePNGRepresentation(imageToSave);
    NSString *filePath = [basePath stringByAppendingPathComponent:@"screenshot_view.png"];
    [binaryImageData writeToFile:filePath atomically:YES];
    filePath;  // Return the NSString as the object to access it's value as the description.
  """.format(args[0])
  target = debugger.GetSelectedTarget()
  if target is None:
    result.Println('ERROR: Could not get selected target.')
    return
  ret_value = target.EvaluateExpression(cmd)
  if not ret_value.GetError().Success():
    result.Println("{0}".format(ret_value.GetError()))
    return
  screenshot_path = ret_value.GetObjectDescription()
  if screenshot_path is None:
    result.Println('ERROR: Screenshot could not be saved.')
    return
  call(['open', screenshot_path])
  result.Println('Screenshot saved:\n' + screenshot_path)

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f screenshot_view.screenshot_view screenshot')
