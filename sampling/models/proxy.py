from .sample import DrillCoreSample, MiningSample

class AcquiredMiningSample(MiningSample):
    class Meta:
        proxy = True

class DrillCore(DrillCoreSample):
    class Meta:
        proxy = True

class DrillCoreAssay(DrillCoreSample):
    class Meta:
        proxy = True

class MiningSampleAssay(MiningSample):
    class Meta:
        proxy = True
