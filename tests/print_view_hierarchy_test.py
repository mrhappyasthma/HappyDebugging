"""Tests for scripts/print_view_hierarchy.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import print_view_hierarchy

class PrintViewHierarchyTest(unittest.TestCase):
  def testPrintViewHierarchy(self):
    """Tests the expected output of the |pv| command."""
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
    print_view_hierarchy.print_view_hierarchy(debugger, None, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex =  r'<UIWindow: 0x\w{12}; frame = \(0 0; \w{3} \w{3}\); autoresize = W\+H; gestureRecognizers = <NSArray: 0x\w{12}>; layer = <UIWindowLayer: 0x\w{12}>>\n   \|'
    self.assertTrue(re.search(expected_output_regex, result.GetOutput(), re.M))
    debugger.DeleteTarget(target)
