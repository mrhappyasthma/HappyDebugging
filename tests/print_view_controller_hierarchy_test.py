"""Tests for scripts/print_view_controller_hierarchy.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import print_view_controller_hierarchy

class PrintViewControllerHierarchyTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(PrintViewControllerHierarchyTest, self).__init__(*args, **kwargs)
    self.debugger = None
    self.target = None

  def tearDown(self):
    if self.debugger and self.target:
      self.debugger.DeleteTarget(self.target)

  def testPrintViewControllerHierarchy(self):
    """Tests the expected output of the |pvc| command."""
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
    print_view_controller_hierarchy.print_view_controller_hierarchy(
        self.debugger, None, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex =  r'<ViewController 0x\w{12}>, state: appeared, view: <UIView 0x\w{12}>'
    self.assertTrue(re.match(expected_output_regex,
                    result.GetOutput().rstrip()))
