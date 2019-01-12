class EnvironmentChecks:
  """A class of utility methods for checking the Target/Build environment."""

  @classmethod
  def _getArchitectureFromTarget(cls, target):
    """Parses the architecture from a given SBTarget.

    @param target An SBTarget instance.
    """
    # Format of the triple is `arch-vendor-os` (e.g. arm64-apple-ios10.0.0).
    triple = target.GetTriple()
    index = triple.index('-')
    return triple[:index]

  @classmethod
  def is32BitSimulatorTarget(cls, target):
    return (cls._getArchitectureFromTarget(target) == 'i386')

  @classmethod
  def is64BitSimulatorTarget(cls, target):
    return (cls._getArchitectureFromTarget(target) == 'x86_64')

  @classmethod
  def is32BitDeviceTarget(cls, target):
    return (cls._getArchitectureFromTarget(target) == 'arm7')

  @classmethod
  def is64BitDeviceTarget(cls, target):
    return (cls._getArchitectureFromTarget(target) == 'arm64')

  @classmethod
  def is32BitTarget(cls, target):
    return (cls.is32BitSimulatorTarget(target) or cls.is32BitDeviceTarget(target))

  @classmethod
  def is64BitTarget(cls, target):
    return (cls.is64BitSimulatorTarget(target) or cls.is64BitDeviceTarget(target))

  @classmethod
  def isSimulatorTarget(cls, target):
    return (cls.is32BitSimulatorTarget(target) or cls.is64BitSimulatorTarget(target))

  @classmethod
  def isDeviceTarget(cls, target):
    return (cls.is32BitDeviceTarget(target) or cls.is64BitDeviceTarget(target))
