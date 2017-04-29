import glob
import os

def __lldb_init_module(debugger, internal_dict):
  scripts_wildcard = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'scripts/*.py')
  scripts = glob.glob(scripts_wildcard)
  for script in scripts:
    debugger.HandleCommand('command script import ' + script)
