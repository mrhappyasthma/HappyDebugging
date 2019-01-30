import lldb
import shlex

from helpers.environment_checks import EnvironmentChecks
from subprocess import call

def accessibility_tree(debugger, command, result, internal_dict):
  """Prints a recursive tree of accessibility elements for a given object.

  Note: This command can only be run while VoiceOver is running.

  Warning: This command uses private framework APIs. Later OS versions may
  cause this command to malfunction.

  Usage:
    accesibilityTree <NSObject_instance>
  """
  args = shlex.split(command)
  if len(args) != 1:
    result.Println('ERROR: Please enter the command as "accessibilityTree <NSObject instance>".')
    return

  if EnvironmentChecks.isSimulatorTarget(debugger.GetSelectedTarget()):
    result.Println('ERROR: This command is only supported for device builds, and current debugger target is a simulator.')
    return

  # Check if private UIAccessibility.framework is already loaded, if not try to load it.
  is_framework_loaded_cmd = """
    @import UIKit;

    BOOL frameworkAlreadyLoaded = NO;
    for (NSBundle *bundle in NSBundle.allFrameworks) {
      NSString *frameworkPath = @"/System/Library/PrivateFrameworks/UIAccessibility.framework";
      if ([bundle.resourcePath isEqualToString:frameworkPath]) {
        frameworkAlreadyLoaded = YES;
        break;
      }
    }
    frameworkAlreadyLoaded
  """
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(is_framework_loaded_cmd, temp_result)
  # If something went wrong, try to load the command.
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    load_framework_cmd = """
      NSString *frameworkPath = @"/System/Library/PrivateFrameworks/UIAccessibility.framework";
      NSBundle *bundle = [NSBundle bundleWithPath:frameworkPath];
      BOOL success = [bundle load];
      success
    """
    temp_result = lldb.SBCommandReturnObject()
    debugger.GetCommandInterpreter().HandleCommand(load_framework_cmd, temp_result)
    if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
      result.Println('ERROR: Could not load the private UIAccessibility.framework.')
      return

  # Ensure we have an NSObject instance. If not, return and print an error message.
  nsobject_check_cmd = 'po (BOOL)[' + args[0] + ' isKindOfClass:[NSObject class]]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(nsobject_check_cmd, temp_result)
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: This command only works for NSObjects. Enter the command as "accessibilitytree <NSObject instance>".')
    return

  # Ensure the object responds to the selector.
  responds_to_selector_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:NSSelectorFromString(@"_accessibilityTreeAsString")]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_cmd, temp_result)
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: Object does not respond to `_accessibilityTreeAsString`. Apple might have changed their API. Please file a bug at http://www.github.com/mrhappyasthma/HappyDebugging')
    return

  cmd = 'po (NSString *)[' + args[0] + ' _accessibilityTreeAsString]'
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  cmd = ('command script add '
         '-f accessibility_tree.accessibility_tree accessibilityTree '
         '-h "Prints a recursive tree of accessibility elements for a given object."')
  debugger.HandleCommand(cmd)
