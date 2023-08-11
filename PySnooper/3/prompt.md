# Prompt

You need to fix a bug in a python code snippet, which got error on line 8, the compiler can't find variable 'output_path'. You need to provide a drop-in replacement, which means minimum changes to source code to pass failed test while won't affect other passed tests. And the fixed patch can be directly used in original project.
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

# LLM Answer

It seems like the issue here is that the variable output_path is not defined in the code, leading to an error on line 8. To fix this issue while making minimal changes to the code, you can replace output_path with output in the second case where you are writing to a file. Here's the corrected code:

    def get_write_function(output):
        if output is None:
            def write(s):
                stderr = sys.stderr
                stderr.write(s)
        elif isinstance(output, (pycompat.PathLike, str)):
            def write(s):
                with open(output, 'a') as output_file:  # Change output_path to output
                    output_file.write(s)
        else:
            assert isinstance(output, utils.WritableStream)
            def write(s):
                output.write(s)

        return write

In this corrected version of the code, the only change made is on line 8, where output_path is replaced with output since you're using output as the file path. This should fix the error on line 8 while keeping the rest of the code and logic intact.

# Fix commit link

https://github.com/cool-RR/PySnooper/commit/15555ed760000b049aff8fecc79d29339c1224c3