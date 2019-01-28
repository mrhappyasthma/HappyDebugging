"""Tests for scripts/helpers/environment_checks.py"""
import unittest

from test_utils import import_utils

import_utils.prepare_for_scripts_imports()

from scripts.helpers.environment_checks import EnvironmentChecks

class DummyTarget:
  """A class that models SBTarget to use within this test. Takes a validly
  formatted `triple` during initialization.
  """

  def __init__(self, triple):
    self.triple = triple

  def GetTriple(self):
    return self.triple

class EnvironmentChecksTest(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(EnvironmentChecksTest, self).__init__(*args, **kwargs)
    self.dummy32BitSimulatorTarget = DummyTarget('i386-apple-ios10.0.0')
    self.dummy64BitSimulatorTarget = DummyTarget('x86_64-apple-ios10.0.0')
    self.dummy32BitDeviceTarget = DummyTarget('armv7-apple-ios10.0.0')
    self.dummy64BitDeviceTarget = DummyTarget('arm64-apple-ios10.0.0')

  def testIsTarget32BitSimulatorBuild(self):
    self.assertTrue(EnvironmentChecks.is32BitSimulatorTarget(self.dummy32BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is32BitSimulatorTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is32BitSimulatorTarget(self.dummy32BitDeviceTarget))
    self.assertFalse(EnvironmentChecks.is32BitSimulatorTarget(self.dummy64BitDeviceTarget))

  def testIsTarget64BitSimulatorBuild(self):
    self.assertFalse(EnvironmentChecks.is64BitSimulatorTarget(self.dummy32BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.is64BitSimulatorTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is64BitSimulatorTarget(self.dummy32BitDeviceTarget))
    self.assertFalse(EnvironmentChecks.is64BitSimulatorTarget(self.dummy64BitDeviceTarget))

  def testIsTarget32BitDeviceBuild(self):
    self.assertFalse(EnvironmentChecks.is32BitDeviceTarget(self.dummy32BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is32BitDeviceTarget(self.dummy64BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.is32BitDeviceTarget(self.dummy32BitDeviceTarget))
    self.assertFalse(EnvironmentChecks.is32BitDeviceTarget(self.dummy64BitDeviceTarget))

  def testIsTarget64BitDeviceBuild(self):
    self.assertFalse(EnvironmentChecks.is64BitDeviceTarget(self.dummy32BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is64BitDeviceTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is64BitDeviceTarget(self.dummy32BitDeviceTarget))
    self.assertTrue(EnvironmentChecks.is64BitDeviceTarget(self.dummy64BitDeviceTarget))

  def testIs32BitTarget(self):
    self.assertTrue(EnvironmentChecks.is32BitTarget(self.dummy32BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is32BitTarget(self.dummy64BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.is32BitTarget(self.dummy32BitDeviceTarget))
    self.assertFalse(EnvironmentChecks.is32BitTarget(self.dummy64BitDeviceTarget))

  def testIs64BitTarget(self):
    self.assertFalse(EnvironmentChecks.is64BitTarget(self.dummy32BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.is64BitTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is64BitTarget(self.dummy32BitDeviceTarget))
    self.assertTrue(EnvironmentChecks.is64BitTarget(self.dummy64BitDeviceTarget))

  def testIs64BitTarget(self):
    self.assertFalse(EnvironmentChecks.is64BitTarget(self.dummy32BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.is64BitTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.is64BitTarget(self.dummy32BitDeviceTarget))
    self.assertTrue(EnvironmentChecks.is64BitTarget(self.dummy64BitDeviceTarget))

  def testIsSimulatorTarget(self):
    self.assertTrue(EnvironmentChecks.isSimulatorTarget(self.dummy32BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.isSimulatorTarget(self.dummy64BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.isSimulatorTarget(self.dummy32BitDeviceTarget))
    self.assertFalse(EnvironmentChecks.isSimulatorTarget(self.dummy64BitDeviceTarget))

  def testIsDeviceTarget(self):
    self.assertFalse(EnvironmentChecks.isDeviceTarget(self.dummy32BitSimulatorTarget))
    self.assertFalse(EnvironmentChecks.isDeviceTarget(self.dummy64BitSimulatorTarget))
    self.assertTrue(EnvironmentChecks.isDeviceTarget(self.dummy32BitDeviceTarget))
    self.assertTrue(EnvironmentChecks.isDeviceTarget(self.dummy64BitDeviceTarget))

