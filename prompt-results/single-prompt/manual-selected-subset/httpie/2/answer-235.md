First, I suggest adding 'max_redirects' as an optional parameter with a default value of None in the get_response function. Then, update the calls to get_requests_kwargs and requests_session.request as shown below:

```python
def get_response(args, config_dir, max_redirects=None):
    """Send the request and return a `request.Response`."""

    requests_session = get_requests_session()

    if not args.session and not args.session_read_only:
        kwargs = get_requests_kwargs(args)
        if max_redirects is not None:
            kwargs["max_redirects"] = max_redirects
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
```

Now, you need to pass the 'max_redirects' value to the 'get_response' function in the test (test_redirects.py). Update the test_max_redirects function as shown below:

```python
def test_max_redirects(httpbin):
    url = URL(httpbin.url).join('/redirect/3')
    max_redirects = 2
    r = http(args=['--max-redirects', str(max_redirects), url], config_dir='.')
    assert r.exit_status == ExitStatus.ERROR_TOO_MANY_REDIRECTS
```

This should fix the bug, without impacting other functionalities. The test_max_redirects function will now pass the max_redirects value to the get_response function, and it should be limited to 2 redirects as expected.