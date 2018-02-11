"""Tests for scripts/pbounds.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import pbounds

class PBoundsTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(PBoundsTest, self).__init__(*args, **kwargs)
    self.debugger = None
    self.target = None

  def tearDown(self):
    if self.debugger and self.target:
      self.debugger.DeleteTarget(self.target)

  def testPFrame(self):
    """Tests the expected output of the |pbounds <instance>| command."""
    self.debugger = lldb.SBDebugger.Create()
    self.debugger.SetAsync(False)
    self.target = self.debugger.CreateTarget('')
    error = lldb.SBError()
    process = self.target.AttachToProcessWithName(self.debugger.GetListener(),
                                                  'TestApp', False, error)
    if not process:
      self.assertTrue(False, 'Could not attach to process "TestApp"')
    self.debugger.SetSelectedTarget(self.target)
    result = lldb.SBCommandReturnObject()

    # Get the test view, which has an abitrary tag of 19.
    self.debugger.GetCommandInterpreter().HandleCommand(
        'po [[UIWindow keyWindow] viewWithTag:19]', result)
    self.assertTrue(result.Succeeded())
    output = result.GetOutput()
    start_index = output.find('0x')
    self.assertTrue(start_index != -1)
    end_index = output.find(';')
    self.assertTrue(end_index != -1)
    view = output[start_index:end_index]

    pbounds.pbounds(self.debugger, view, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex = r'\(origin = \(x = 0, y = 0\), size = \(width = 100, height = 100\)\)'
    self.assertTrue(re.search(expected_output_regex, result.GetOutput(), re.M))
