You need to fix a bug in a python code snippet, which failed on test.

The buggy source code is following:

    def get_response(args, config_dir):
        """Send the request and return a `request.Response`."""

        requests_session = get_requests_session()

        if not args.session and not args.session_read_only:
            kwargs = get_requests_kwargs(args)
            if args.debug:
                dump_request(kwargs)
            response = requests_session.request(**kwargs)
        else:
            response = sessions.get_response(
                requests_session=requests_session,
                args=args,
                config_dir=config_dir,
                session_name=args.session or args.session_read_only,
                read_only=bool(args.session_read_only),
            )

        return response

Part of definition of Session class is:

    class Session(SessionRedirectMixin):
        """A Requests session.

        Provides cookie persistence, connection-pooling, and configuration.

        Basic Usage::

        >>> import requests
        >>> s = requests.Session()
        >>> s.get('https://httpbin.org/get')
        <Response [200]>

        Or as a context manager::

        >>> with requests.Session() as s:
        ...     s.get('https://httpbin.org/get')
        <Response [200]>
        """

        __attrs__ = [
            "headers",
            "cookies",
            "auth",
            "proxies",
            "hooks",
            "params",
            "verify",
            "cert",
            "adapters",
            "stream",
            "trust_env",
            "max_redirects",
        ]

The test source code is following:

    def test_max_redirects(self, httpbin):
        r = http('--max-redirects=2', '--follow', httpbin.url + '/redirect/3',
                 error_exit_ok=True)
        assert r.exit_status == ExitStatus.ERROR_TOO_MANY_REDIRECTS


The test error on command line is following:
=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.7.16, pytest-3.2.1, py-1.11.0, pluggy-0.4.0
rootdir: /Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:2, inifile: pytest.ini
plugins: timeout-1.2.1, httpbin-2.0.0
timeout: 10.0s method: signal
collected 1 item                                                                                                                                                                                            
 
tests/test_redirects.py F
 
================================================================================================= FAILURES =================================================================================================
_____________________________________________________________________________________ TestRedirects.test_max_redirects _____________________________________________________________________________________
Traceback (most recent call last):
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:2/tests/test_redirects.py", line 22, in test_max_redirects
    assert r.exit_status == ExitStatus.ERROR_TOO_MANY_REDIRECTS
AssertionError: assert 0 == 6
 +  where 0 = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Credentials: true\r\nAccess-Control-Allow-Origin: *\r\nConnection: Close\r\nC...  "User-Agent": "HTTPie/1.0.0-dev"\n    },\n    "origin": "127.0.0.1",\n    "url": "http://127.0.0.1:50270/get"\n}\n\n'.exit_status
 +  and   6 = ExitStatus.ERROR_TOO_MANY_REDIRECTS
------------------------------------------------------------------------------------------- Captured stderr call -------------------------------------------------------------------------------------------
127.0.0.1 - - [17/Aug/2023 19:05:51] "GET /redirect/3 HTTP/1.1" 302 227
127.0.0.1 - - [17/Aug/2023 19:05:51] "GET /relative-redirect/2 HTTP/1.1" 302 0
127.0.0.1 - - [17/Aug/2023 19:05:51] "GET /relative-redirect/1 HTTP/1.1" 302 0
127.0.0.1 - - [17/Aug/2023 19:05:51] "GET /get HTTP/1.1" 200 266
========================================================================================= 1 failed in 0.68 seconds =========================================================================================


And the raised issue description for this bug is 'I think we should have an 'option' to set max redirect'.


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.