"""A collection of helper utilities for importing modules in tests."""
import sys


def prepare_for_scripts_imports():
  """Gets the test in a state where it can import directly from the |scripts|
  dir."""
  import os
  scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
  sys.path.append(scripts_path);


def prepare_lldb_import_or_exit():
  """Attempts to import lldb. If it fails, it prints an error."""
  try:
    import subprocess
    lldb_path = subprocess.check_output(['lldb', '-P'])
    lldb_path = lldb_path[:-1]  # Remove the trailing newline character.
    sys.path.append(lldb_path)
  except:
    print 'ERROR: Cannot run |lldb -P| to determine the necessary import path.'
    sys.exit(1)
