To fix the bug, you need to ensure that the `value` is not of `NoneType` before trying to decode it. You can add a simple condition to the `update_headers` function to check if the value is `None` before decoding. Here's the modified code with the fix:

```python
	def update_headers(self, request_headers):
		"""
		Update the session headers with the request ones while ignoring
		certain name prefixes.

		:type request_headers: dict

		"""
		for name, value in request_headers.items():
			if value is not None:
				value = value.decode('utf8')
			if name == 'User-Agent' and value.startswith('HTTPie/'):
				continue

			for prefix in SESSION_IGNORED_HEADER_PREFIXES:
				if name.lower().startswith(prefix.lower()):
					break
				else:
					self['headers'][name] = value
```

This change should fix the 'AttributeError: 'NoneType' object has no attribute 'decode' on --download' issue without affecting other tests.