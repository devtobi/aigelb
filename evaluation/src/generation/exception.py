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
