"""Tests for scripts/ivars.py."""
import re
import unittest

from test_utils import import_utils
import_utils.prepare_lldb_import_or_exit()

import lldb

import_utils.prepare_for_scripts_imports()

from scripts import ivars

class IvarsTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(IvarsTest, self).__init__(*args, **kwargs)
    self.debugger = None
    self.target = None

  def tearDown(self):
    if self.debugger and self.target:
      self.debugger.DeleteTarget(self.target)


  def testIvars(self):
    """Tests the expected output of the |ivars <object>| command."""
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

    # First get the AppDelegate object, whose ivars we will use to test
    # the command.
    #
    # The output is in the format |<AppDelegate: 0x7fd704401810>|.
    self.debugger.GetCommandInterpreter().HandleCommand(
        'po [[UIApplication sharedApplication] delegate]', result)
    self.assertTrue(result.Succeeded())
    output = result.GetOutput()
    start_index = output.find('0x')
    self.assertTrue(start_index != -1)
    end_index = output.find('>')
    self.assertTrue(end_index != -1)
    delegate = output[start_index:end_index]

    ivars.ivars(self.debugger, delegate, result, None)
    self.assertTrue(result.Succeeded())
    expected_output_regex = (
        r'<__NSArrayM 0x\w{12}>\(\n'
        r'\(NSString \*\) _test -> 0x\w{9},\n'
        r'\(int\) _x,\n'
        r'\(int\*\*\) _ptr,\n'
        r'\(int\[5\]\) _y,\n'
        r'\(id const \*\) _temp,\n'
        r'\(id\) _something -> nil,\n'
        r'\(struct DummyStruct\[4\]\) _t,\n'
        r'\(struct DummyStruct\*\) _example,\n'
        r'\(union DummyUnion\) _someUnion,\n'
        r'\(~block~\) _myBlock -> 0x\w{9},\n'
        r'\(~block~\) _myBlockEmpty -> nil,\n'
        r'\(~function pointer~\) _myPointer,\n'
        r'\(UIWindow \*\) _window -> 0x\w{12}\n'
        r'\)'
    )

    self.assertTrue(re.search(expected_output_regex,
                    result.GetOutput(), re.M))
