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



The raised issue description for this bug is: 'AttributeError: 'NoneType' object has no attribute 'decode' on --download'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.