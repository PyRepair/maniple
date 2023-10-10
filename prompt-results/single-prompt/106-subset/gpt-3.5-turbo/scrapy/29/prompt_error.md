You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

def request_httprepr(request):
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s



The test error on command line is following:

======================================================================
ERROR: test_request_httprepr_for_non_http_request (tests.test_utils_request.UtilsRequestTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:29/tests/test_utils_request.py", line 76, in test_request_httprepr_for_non_http_request
    request_httprepr(Request("file:///tmp/foo.txt"))
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:29/scrapy/utils/request.py", line 82, in request_httprepr
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:29/scrapy/utils/python.py", line 116, in to_bytes
    raise TypeError('to_bytes must receive a unicode, str or bytes '
TypeError: to_bytes must receive a unicode, str or bytes object, got NoneType

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)


