from core.common.helper.exception_helper import ExceptionHelper


class DatabaseQueryError(ExceptionHelper, Exception):

    def __init__(self, message, code=None):
        super(DatabaseQueryError, self).__init__(message, code=code)


class JoinQueryError(DatabaseQueryError):
    """ join error """


class WhereQueryError(DatabaseQueryError):
    """ where error """


class LimitQueryError(DatabaseQueryError):
    """ limit error """


class GroupByQueryError(DatabaseQueryError):
    """ group by error """


class HavingQueryError(DatabaseQueryError):
    """ having error """


class OrderByQueryError(DatabaseQueryError):
    """ order by error """


class SelectExecutionError(DatabaseQueryError):
    """ select execution error """


class DeleteExecutionError(DatabaseQueryError):
    """ delete execution error """


class InsertExecutionError(DatabaseQueryError):
    """ insert execution error """


class UpdateExecutionError(DatabaseQueryError):
    """ update execution error """
