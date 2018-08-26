import glob
import lldb
import os

def Println(self, *args):
  self.Print(args[0] + '\n')

def __lldb_init_module(debugger, internal_dict):
  # Add a custom print function to SBCommandReturnObject.
  lldb.SBCommandReturnObject.Println = Println

  # Load all of the lldb scripts.
  scripts_wildcard = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'scripts/*.py')
  scripts = glob.glob(scripts_wildcard)
  for script in scripts:
    debugger.HandleCommand('command script import ' + script)
