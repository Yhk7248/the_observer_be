
class ExceptionHelper(object):
    # TODO: mysql db 에러 넘버 정의 필요
    code = None

    def __init__(self, *arg, **kw):
        code = kw.pop("code", None)
        if code is not None:
            self.code = code
        super(ExceptionHelper, self).__init__(*arg, **kw)

    def __str__(self):
        message = super(ExceptionHelper, self).__str__()
        if self.code:
            message = "%s %s" % (message, self.code)
        return message


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
