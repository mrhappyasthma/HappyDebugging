"""Tests for scripts/print_view_controller_hierarchy.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import print_view_controller_hierarchy

class PrintViewControllerHierarchyTest(unittest.TestCase):
  def testPrintViewControllerHierarchy(self):
    """Tests the expected output of the |pvc| command."""
    debugger = lldb.SBDebugger.Create()
    debugger.SetAsync(False)
    target = debugger.CreateTarget('')
    error = lldb.SBError()
    process = target.AttachToProcessWithName(debugger.GetListener(), 'TestApp',
                                             False, error)
    if not process:
      self.assertTrue(False, 'Could not attach to process "TestApp"')
    debugger.SetSelectedTarget(target)
    result = lldb.SBCommandReturnObject()
    print_view_controller_hierarchy.print_view_controller_hierarchy(debugger,
                                                                    None,
                                                                    result,
                                                                    None)
    self.assertTrue(result.Succeeded())
    expected_output_regex =  r'<ViewController 0x\w{12}>, state: appeared, view: <UIView 0x\w{12}>'
    self.assertTrue(re.match(expected_output_regex,
                    result.GetOutput().rstrip()))
    debugger.DeleteTarget(target)
