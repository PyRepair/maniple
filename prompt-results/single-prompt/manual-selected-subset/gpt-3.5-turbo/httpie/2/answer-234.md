The problem here seems to be the lack of handling for maximum redirects in the request.

The `get_response` function should check if the maximum redirects limit has been reached which is not implemented in the provided code.

We would need to implement a check for `args.max_redirects` to the `get_requests_kwargs` function as follows - 

	def get_requests_kwargs(args):
		kwargs = {
			# other kwargs
			'allow_redirects': args.follow,
			'max_redirects': args.max_redirects if hasattr(args, 'max_redirects') else None
		}
		return kwargs

and update the `get_response` function 

	def get_response(args, config_dir):
		"""Send the request and return a `request.Response`."""

		requests_session = get_requests_session()

		if not args.session and not args.session_read_only:
			kwargs = get_requests_kwargs(args)
			
			if args.debug:
				dump_request(kwargs)

			try:
				response = requests_session.request(**kwargs)
			except requests.exceptions.TooManyRedirects:
				exit_status = ExitStatus.ERROR_TOO_MANY_REDIRECTS 
				return exit_status
		else:
			response = sessions.get_response(
				requests_session=requests_session,
				args=args,
				config_dir=config_dir,
				session_name=args.session or args.session_read_only,
				read_only=bool(args.session_read_only),
			)

		return response

The fixed implementation checks for an attribute `max_redirects` in args (checking with `hasattr` to avoid a `AttributeError` if it doesn't exist). It then passes this value as an argument to the request call. If a `requests.exceptions.TooManyRedirects` exception is raised, it sets the exit status to `ExitStatus.ERROR_TOO_MANY_REDIRECTS`.

Please make sure to import `ExitStatus` and `requests` at the beginning of your file:

	from httpie.status import ExitStatus
	import requests