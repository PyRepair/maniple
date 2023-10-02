You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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



Part of class definition that might be helpful for fixing bug is:

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
		...	 s.get('https://httpbin.org/get')
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



The raised issue description for this bug is: 'I think we should have an 'option' to set max redirect'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.