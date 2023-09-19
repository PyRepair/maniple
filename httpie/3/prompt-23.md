You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

	def update_headers(self, request_headers):
		"""
		Update the session headers with the request ones while ignoring
		certain name prefixes.

		:type request_headers: dict

		"""
		for name, value in request_headers.items():
			value = value.decode('utf8')
			if name == 'User-Agent' and value.startswith('HTTPie/'):
				continue

			for prefix in SESSION_IGNORED_HEADER_PREFIXES:
				if name.lower().startswith(prefix.lower()):
					break
				else:
					self['headers'][name] = value



The test error on command line is following:

=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.7.16, pytest-3.2.1, py-1.11.0, pluggy-0.4.0
rootdir: /Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3, inifile: pytest.ini
plugins: timeout-1.2.1, httpbin-2.0.0
timeout: 10.0s method: signal
collected 1 item

tests/test_sessions.py F

================================================================================================= FAILURES =================================================================================================
___________________________________________________________________________________ TestSession.test_download_in_session ___________________________________________________________________________________
Traceback (most recent call last):
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/tests/test_sessions.py", line 186, in test_download_in_session
    httpbin.url + '/get', env=self.env()
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/tests/utils.py", line 136, in http
    exit_status = main(args=args, **kwargs)
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/httpie/core.py", line 115, in main
    response = get_response(args, config_dir=env.config.directory)
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/httpie/client.py", line 55, in get_response
    read_only=bool(args.session_read_only),
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/httpie/sessions.py", line 52, in get_response
    session.update_headers(kwargs['headers'])
  File "/Users/nikhilparasaram/Work/PyRepair/benchmarks/BugsInPy_REPOS/httpie:3/httpie/sessions.py", line 104, in update_headers
    value = value.decode('utf8')
AttributeError: 'NoneType' object has no attribute 'decode'
========================================================================================= 1 failed in 0.63 seconds =========================================================================================
Error: Command '['venv/bin/python3.7', '-m', 'pytest', 'tests/test_sessions.py::TestSession::test_download_in_session', '--timeout=10']' returned non-zero exit status 1.



The test source code is following:

	def test_download_in_session(self, tmp_path, httpbin):
		# https://github.com/httpie/cli/issues/412
		self.start_session(httpbin)
		cwd = os.getcwd()
		os.chdir(tmp_path)
		try:
			http('--session=test', '--download',
				 httpbin.url + '/get', env=self.env())
		finally:
			os.chdir(cwd)



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.