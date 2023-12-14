def eb_wrapper(failure):
    case = _create_testcase(method, 'errback')
    exc_info = failure.type, failure.value, failure.getTracebackObject()
    results.addError(case, exc_info)


request.callback = cb_wrapper
request.errback = eb_wrapper
