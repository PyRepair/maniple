This `_on_access_token` function has a bug, can you help to the write the whole fixed `_on_access_token` function implementation?

buggy code:

```python
from __future__ import absolute_import, division, print_function, with_statement

import base64
import binascii
import functools
import hashlib
import hmac
import time
import uuid

from tornado.concurrent import TracebackFuture, return_future, chain_future
from tornado import gen
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.log import gen_log
from tornado.stack_context import ExceptionStackContext
from tornado.util import u, unicode_type, ArgReplacer

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    import urllib.parse as urllib_parse  # py3
except ImportError:
    import urllib as urllib_parse  # py2

try:
    long  # py2
except NameError:
    long = int  # py3


class FacebookGraphMixin(OAuth2Mixin):

    # ... other methods ...

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Facebook auth error: %s' % str(response)))
            return

        args = escape.parse_qs_bytes(escape.native_str(response.body))
        session = {
            "access_token": args["access_token"][-1],
            "expires": args.get("expires")
        }

        self.facebook_request(
            path="/me",
            callback=functools.partial(
                self._on_get_user_info, future, session, fields),
            access_token=session["access_token"],
            fields=",".join(fields)
        )
```

The issue message is:

```text
I had to modify _on_access_token so that it did not attempt to make a facebook_request to /me. With the code as it stands, I get this error:

TypeError: 'Future' object is not callable

However, removing that extra request fixes this, and I can use the access_token in the next part of my auth pipeline.
```

the test code is:

```python
from __future__ import absolute_import, division, print_function, with_statement
from tornado.auth import OpenIdMixin, OAuthMixin, OAuth2Mixin, TwitterMixin, AuthError, GoogleOAuth2Mixin, FacebookGraphMixin
from tornado.concurrent import Future
from tornado.escape import json_decode
from tornado import gen
from tornado.httputil import url_concat
from tornado.log import gen_log
from tornado.testing import AsyncHTTPTestCase, ExpectLog
from tornado.util import u
from tornado.web import RequestHandler, Application, asynchronous, HTTPError

class FacebookClientLoginHandler(RequestHandler, FacebookGraphMixin):
    def initialize(self, test):
        self._OAUTH_AUTHORIZE_URL = test.get_url('/facebook/server/authorize')
        self._OAUTH_ACCESS_TOKEN_URL = test.get_url('/facebook/server/access_token')
        self._FACEBOOK_BASE_URL = test.get_url('/facebook/server')

    @gen.coroutine
    def get(self):
        if self.get_argument("code", None):
            user = yield self.get_authenticated_user(
                redirect_uri=self.request.full_url(),
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
            self.write(user)
        else:
                yield self.authorize_redirect(
                    redirect_uri=self.request.full_url(),
                    client_id=self.settings["facebook_api_key"],
                    extra_params={"scope": "read_stream,offline_access"})


class FacebookServerAccessTokenHandler(RequestHandler):
    def get(self):
        self.write('access_token=asdf')


class FacebookServerMeHandler(RequestHandler):
    def get(self):
        self.write('{}')


class AuthTest(AsyncHTTPTestCase):
    def get_app(self):
        return Application(
            [
                # test endpoints
                ('/openid/client/login', OpenIdClientLoginHandler, dict(test=self)),
                ('/oauth10/client/login', OAuth1ClientLoginHandler,
                 dict(test=self, version='1.0')),
                ('/oauth10/client/request_params',
                 OAuth1ClientRequestParametersHandler,
                 dict(version='1.0')),
                ('/oauth10a/client/login', OAuth1ClientLoginHandler,
                 dict(test=self, version='1.0a')),
                ('/oauth10a/client/login_coroutine',
                 OAuth1ClientLoginCoroutineHandler,
                 dict(test=self, version='1.0a')),
                ('/oauth10a/client/request_params',
                 OAuth1ClientRequestParametersHandler,
                 dict(version='1.0a')),
                ('/oauth2/client/login', OAuth2ClientLoginHandler, dict(test=self)),

                ('/facebook/client/login', FacebookClientLoginHandler, dict(test=self)),

                ('/twitter/client/login', TwitterClientLoginHandler, dict(test=self)),
                ('/twitter/client/login_gen_engine', TwitterClientLoginGenEngineHandler, dict(test=self)),
                ('/twitter/client/login_gen_coroutine', TwitterClientLoginGenCoroutineHandler, dict(test=self)),
                ('/twitter/client/show_user', TwitterClientShowUserHandler, dict(test=self)),
                ('/twitter/client/show_user_future', TwitterClientShowUserFutureHandler, dict(test=self)),

                # simulated servers
                ('/openid/server/authenticate', OpenIdServerAuthenticateHandler),
                ('/oauth1/server/request_token', OAuth1ServerRequestTokenHandler),
                ('/oauth1/server/access_token', OAuth1ServerAccessTokenHandler),

                ('/facebook/server/access_token', FacebookServerAccessTokenHandler),
                ('/facebook/server/me', FacebookServerMeHandler),
                ('/twitter/server/access_token', TwitterServerAccessTokenHandler),
                (r'/twitter/api/users/show/(.*)\.json', TwitterServerShowUserHandler),
                (r'/twitter/api/account/verify_credentials\.json', TwitterServerVerifyCredentialsHandler),
            ],
            http_client=self.http_client,
            twitter_consumer_key='test_twitter_consumer_key',
            twitter_consumer_secret='test_twitter_consumer_secret',
            facebook_api_key='test_facebook_api_key',
            facebook_secret='test_facebook_secret')

    def test_facebook_login(self):
        response = self.fetch('/facebook/client/login', follow_redirects=False)
        self.assertEqual(response.code, 302)
        self.assertTrue('/facebook/server/authorize?' in response.headers['Location'])
        response = self.fetch('/facebook/client/login?code=1234', follow_redirects=False)
        self.assertEqual(response.code, 200)
```

the error message is:

```text
ERROR:tornado.application:Exception in callback functools.partial(<function _auth_future_to_callback at 0x7fbda7c72b90>, <tornado.concurrent.Future object at 0x7fbda9363d50>) for <tornado.concurrent.Future object at 0x7fbda93639d0>
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/concurrent.py", line 317, in _set_done
    cb(self)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/auth.py", line 113, in _auth_future_to_callback
    callback(result)
TypeError: 'Future' object is not callable
======================================================================
FAIL: test_facebook_login (tornado.test.auth_test.AuthTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/testing.py", line 125, in __call__
    result = self.orig_method(*args, **kwargs)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/test/auth_test.py", line 403, in test_facebook_login
    response = self.fetch('/facebook/client/login?code=1234', follow_redirects=False)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/testing.py", line 395, in fetch
    return self.wait()
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/testing.py", line 325, in wait
    self.__rethrow()
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/testing.py", line 261, in __rethrow
    raise_exc_info(failure)
  File "<string>", line 3, in raise_exc_info
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/tornado/12/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:12/tornado/testing.py", line 309, in timeout_func
    timeout)
AssertionError: Async operation timed out after 5 seconds
```


You should provide answer with following steps: 
1. Understand test and relationship between test code and error message 
2. Find a possible error location inside buggy function 
3. Reasoning why the bug appears 
4. Suggest possible minimal fix method 
5. Always provide full function code for fixed buggy function.
