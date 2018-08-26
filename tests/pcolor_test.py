"""Tests for scripts/pcolor.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import pcolor

class PColorTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(PColorTest, self).__init__(*args, **kwargs)
    self.debugger = None
    self.target = None

  def tearDown(self):
    if self.debugger and self.target:
      self.debugger.DeleteTarget(self.target)

  def testPColor(self):
    """Tests the expected output of the |pcolor <UIColor_instance>| command."""
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

    pcolor.pcolor(self.debugger, '[UIColor blueColor]', result, None)
    expected_output = 'RGBA = 0, 0, 255, 1.0000\nHex = #0000ff\n'
    self.assertEqual(result.GetOutput(), expected_output)
