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
