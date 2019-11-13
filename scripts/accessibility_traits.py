import lldb
import shlex

from helpers.environment_checks import EnvironmentChecks
from subprocess import call

def accessibility_traits(debugger, command, result, internal_dict):
    """Prints human readable strings of the a11y traits for a given object..

  Note: This command can only be run while VoiceOver is running.

  Warning: This command uses private framework APIs. Later OS versions may
  cause this command to malfunction.

  Usage:
    accesibilityTraits <NSObject_instance>
  """
  args = shlex.split(command)
  if len(args) != 1:
    result.Println('ERROR: Please enter the command as "accessibilityTraits <NSObject instance>".')
    return

  target = debugger.GetSelectedTarget()
  if target is None:
    result.Println('ERROR: Could not get selected target.')
    return
  if EnvironmentChecks.isSimulatorTarget(target):
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
    frameworkAlreadyLoaded ? @"YES" : @"NO";  // Return the BOOL
  """
  ret_value = target.EvaluateExpression(is_framework_loaded_cmd)
  # If something went wrong, try to load the command.
  if not ret_value.GetError().Success() or ret_value.GetObjectDescription().strip() == 'NO':
    load_framework_cmd = """
      NSString *frameworkPath = @"/System/Library/PrivateFrameworks/UIAccessibility.framework";
      NSBundle *bundleForFramework = [NSBundle bundleWithPath:frameworkPath];
      BOOL success = [bundleForFramework load];
      success ? @"YES" : @"NO";  // Return the BOOL
    """
    ret_value = target.EvaluateExpression(load_framework_cmd)
    result.Println(ret_value.GetError().GetCString())
    if not ret_value.GetError().Success() or ret_value.GetObjectDescription().strip() == 'NO':
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
  responds_to_selector_cmd = 'po (BOOL)[' + args[0] + ' respondsToSelector:NSSelectorFromString(@"_accessibilityTraitsInspectorHumanReadable")]'
  temp_result = lldb.SBCommandReturnObject()
  debugger.GetCommandInterpreter().HandleCommand(responds_to_selector_cmd, temp_result)
  if temp_result.GetError() or temp_result.GetOutput().strip() == 'NO':
    result.Println('ERROR: Object does not respond to `_accessibilityTraitsInspectorHumanReadable`. Apple might have changed their API. Please file a bug at http://www.github.com/mrhappyasthma/HappyDebugging')
    return

  cmd = 'po (NSString *)[' + args[0] + ' _accessibilityTraitsInspectorHumanReadable]'
  debugger.GetCommandInterpreter().HandleCommand(cmd, result)

def __lldb_init_module(debugger, internal_dict):
  cmd = ('command script add '
         '-f accessibility_traits.accessibility_traits accessibilityTraits '
         '-h "Prints the a11y traits of the given object as human readable strings."')
  debugger.HandleCommand(cmd)
