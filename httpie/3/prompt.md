# Prompt

You need to fix a bug in a python code snippet, which failed on test on line 10 when value is 'None'. You need to provide a drop-in replacement, which means minimum changes to source code to pass failed test while won't affect other passed tests. And the fixed patch can be directly used in original project.
The buggy source code with comment inside is following:

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

# LLM Answer

To fix the bug in the provided code snippet, specifically the issue when the value is 'None', you can make a minimal change to the code. Here's the modified version of the code snippet:

    def update_headers(self, request_headers):
        """
        Update the session headers with the request ones while ignoring
        certain name prefixes.

        :type request_headers: dict

        """
        for name, value in request_headers.items():
            if value is None:
                continue
            value = value.decode('utf8')
            if name == 'User-Agent' and value.startswith('HTTPie/'):
                continue

            for prefix in SESSION_IGNORED_HEADER_PREFIXES:
                if name.lower().startswith(prefix.lower()):
                    break
            else:
                self['headers'][name] = value

The only change made here is the addition of a condition to check if value is None. If it is None, the loop will continue to the next iteration, skipping the decoding and further checks. This change ensures that the code won't break when encountering a 'None' value for value. The rest of the code remains unchanged to ensure that the fix is minimal and won't affect other parts of the code or passed tests.

# Fix commit link

https://github.com/httpie/cli/commit/589887939507ff26d36ec74bd2c045819cfa3d56