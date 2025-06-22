class GenerationSourcesFileNotFoundError(Exception):
  pass

class GenerationSystemPromptFileNotFoundError(Exception):
  pass

class GenerationUserPromptFileNotFoundError(Exception):
  pass

class GenerationUserPromptFileEmptyError(Exception):
  pass

class GenerationUserPromptFileMissingTemplateError(Exception):
  pass

class GenerationModelNotFoundError(Exception):
  pass

class GenerationModelLoadError(Exception):
  pass

class GenerationModelInferenceError(Exception):
  pass

class GenerationPredictionWriteError(Exception):
  pass
