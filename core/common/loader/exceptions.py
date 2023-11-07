from core.common.helper.exception_helper import ExceptionHelper


class YamlLoadException(ExceptionHelper, Exception):

    message = "An exception occurred while loading the YAML file."

    def __init__(self, code=None):
        super(YamlLoadException, self).__init__(message=self.message, code=code)

