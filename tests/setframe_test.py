"""Tests for scripts/pframe.py.

NOTE: This test assumes that `TestApp` has a UIView with `tag` value
      of 19. That view must have the following frame: {0, 0, 100, 100}.
"""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import pframe
from scripts import set_frame

class SetFrameTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(SetFrameTest, self).__init__(*args, **kwargs)
    self.debugger = None
    self.target = None
    self.view = None

  def tearDown(self):
    if self.debugger and self.target:
      # Set the frame back to the default so that other tests wont be affected.
      params = self.view + ' 0 0 100 100'
      result = lldb.SBCommandReturnObject()
      set_frame.set_frame(self.debugger, params, result, None)
      self.assertTrue(result.Succeeded())
      pframe.pframe(self.debugger, self.view, result, None)
      self.assertTrue(result.Succeeded())
      expected_output_regex = r'\(origin = \(x = 0, y = 0\), size = \(width = 100, height = 100\)\)'
      self.assertTrue(re.match(expected_output_regex, result.GetOutput()))

      # Detach debugger.
      self.debugger.DeleteTarget(self.target)

  def testPFrame(self):
    """Tests the expected output of the |setframe <instance> <x> <y> <width>< height>| command."""
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
    self.view = output[start_index:end_index]

    # Check that the original frame is valid.
    pframe.pframe(self.debugger, self.view, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex = r'\(origin = \(x = 0, y = 0\), size = \(width = 100, height = 100\)\)'
    self.assertTrue(re.match(expected_output_regex, result.GetOutput()))

    # Set a new frame, and check that it's in the output.
    params = self.view + ' 10 10 10 10'
    set_frame.set_frame(self.debugger, params, result, None)
    self.assertTrue(result.Succeeded())
    pframe.pframe(self.debugger, self.view, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex = r'\(origin = \(x = 10, y = 10\), size = \(width = 10, height = 10\)\)'
    self.assertTrue(re.match(expected_output_regex, result.GetOutput()))
