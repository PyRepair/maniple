You need to fix a bug in a python code snippet.

The buggy source code is following:

    def get_write_function(output):
        if output is None:
            def write(s):
                stderr = sys.stderr
                stderr.write(s)
        elif isinstance(output, (pycompat.PathLike, str)):
            def write(s):
                with open(output_path, 'a') as output_file:
                    output_file.write(s)
        else:
            assert isinstance(output, utils.WritableStream)
            def write(s):
                output.write(s)

        return write


And the raised issue description for this bug is 'NameError: global name 'output_path' is not defined'.


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.