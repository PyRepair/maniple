You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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
		headers = '
'.join(headers).strip()

		if isinstance(headers, bytes):
			# Python < 3
			headers = headers.decode('utf8')
		return headers



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
E        +    where <built-in method count of str object at 0x104056a50> = "get /get http/1.1
accept: */*
accept-encoding: gzip, deflate, compress
host: 3.225.120.215
user-agent: b'...ength: 311
content-type: application/json
date: thu, 17 aug 2023 18:18:47 gmt
server: gunicorn/19.9.0

".count
E        +      where "get /get http/1.1
accept: */*
accept-encoding: gzip, deflate, compress
host: 3.225.120.215
user-agent: b'...ength: 311
content-type: application/json
date: thu, 17 aug 2023 18:18:47 gmt
server: gunicorn/19.9.0

" = <built-in method lower of StrCLIResponse object at 0x103f36ed0>()
E        +        where <built-in method lower of StrCLIResponse object at 0x103f36ed0> = "GET /get HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, compress
Host: 3.225.120.215
User-Agent: b'...ength: 311
Content-Type: application/json
Date: Thu, 17 Aug 2023 18:18:47 GMT
Server: gunicorn/19.9.0

".lower

tests/test_regressions.py:17: AssertionError
============================================================================================= warnings summary =============================================================================================



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



The raised issue description for this bug is: 'need specify custom Host'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.