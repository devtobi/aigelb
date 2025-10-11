class CalculationMetricError(Exception):
  pass

class CalculationDataLengthMismatchError(Exception):
  pass

class CalculationResultsWriteError(Exception):
  pass

class CalculationReferenceFileNotFoundError(Exception):
  pass

class CalculationNoReferencesFoundError(Exception):
  pass

class CalculationPredictionsFileNotFoundError(Exception):
  pass
