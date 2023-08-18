# Prompt

You need to fix a bug in a python code snippet.

The buggy source code is following:

    def headers(self):
        url = urlsplit(self._orig.url)

        request_line = '{method} {path}{query} HTTP/1.1'.format(
            method=self._orig.method,
            path=url.path or '/',
            query='?' + url.query if url.query else ''
        )

        headers = dict(self._orig.headers)
        if 'Host' not in headers:
            headers['Host'] = url.netloc.split('@')[-1]

        headers = ['%s: %s' % (name, value)
                   for name, value in headers.items()]

        headers.insert(0, request_line)
        headers = '\r\n'.join(headers).strip()

        if isinstance(headers, bytes):
            # Python < 3
            headers = headers.decode('utf8')
        return headers


The test source code is following:

    def test_Host_header_overwrite():
    """
    https://github.com/jakubroztocil/httpie/issues/235
    """
    host = 'httpbin.org'
    url = 'http://{httpbin_ip}/get'.format(
        httpbin_ip=socket.gethostbyname(host))
    r = http('--print=hH', url, 'host:{}'.format(host))
    assert HTTP_OK in r
    assert r.lower().count('host:') == 1


The test error on command line is following:
================================================================================================= FAILURES =================================================================================================
________________________________________________________________________________________ test_Host_header_overwrite ________________________________________________________________________________________
 
    def test_Host_header_overwrite():
        """
        https://github.com/jakubroztocil/httpie/issues/235
 
        """
        host = 'httpbin.org'
        url = 'http://{httpbin_ip}/get'.format(
            httpbin_ip=socket.gethostbyname(host))
        r = http('--print=hH', url, 'host:{}'.format(host))
        assert HTTP_OK in r
>       assert r.lower().count('host:') == 1
E       assert 2 == 1
E        +  where 2 = <built-in method count of str object at 0x104056a50>('host:')
E        +    where <built-in method count of str object at 0x104056a50> = "get /get http/1.1\r\naccept: */*\r\naccept-encoding: gzip, deflate, compress\r\nhost: 3.225.120.215\r\nuser-agent: b'...ength: 311\r\ncontent-type: application/json\r\ndate: thu, 17 aug 2023 18:18:47 gmt\r\nserver: gunicorn/19.9.0\r\n\r\n".count
E        +      where "get /get http/1.1\r\naccept: */*\r\naccept-encoding: gzip, deflate, compress\r\nhost: 3.225.120.215\r\nuser-agent: b'...ength: 311\r\ncontent-type: application/json\r\ndate: thu, 17 aug 2023 18:18:47 gmt\r\nserver: gunicorn/19.9.0\r\n\r\n" = <built-in method lower of StrCLIResponse object at 0x103f36ed0>()
E        +        where <built-in method lower of StrCLIResponse object at 0x103f36ed0> = "GET /get HTTP/1.1\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate, compress\r\nHost: 3.225.120.215\r\nUser-Agent: b'...ength: 311\r\nContent-Type: application/json\r\nDate: Thu, 17 Aug 2023 18:18:47 GMT\r\nServer: gunicorn/19.9.0\r\n\r\n".lower
 
tests/test_regressions.py:17: AssertionError
============================================================================================= warnings summary =============================================================================================


And the fix commit of the project author is 'Fixed custom Host'.


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.