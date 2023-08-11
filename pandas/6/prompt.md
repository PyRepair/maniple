# Prompt


You need to fix a bug in a python code snippet, which failed on test and got 'ValueError' on line 5. You need to provide a drop-in replacement, which means minimum changes to source code to pass failed test while won't affect other passed tests. And the fixed patch can be directly used in original project.
The buggy source code is following:

    def is_in_obj(gpr) -> bool:
        if not hasattr(gpr, "name"):
            return False
        try:
            return gpr is obj[gpr.name]
        except (KeyError, IndexError):
            return False

# LLM Answer

The bug in the provided code snippet seems to be related to the usage of the obj variable without it being defined anywhere. To fix this issue and provide a drop-in replacement, you can modify the code as follows:

    def is_in_obj(gpr, obj) -> bool:
        if not hasattr(gpr, "name"):
            return False
        try:
            return gpr is obj[gpr.name]
        except (KeyError, IndexError):
            return False

In this fixed version of the code, I added an additional parameter obj to the is_in_obj function, which should be passed when calling the function. This will ensure that the obj dictionary is accessible within the function and the code should work as intended. Make sure to update your function calls to provide the obj parameter as well.

# Fix commit link

https://github.com/pandas-dev/pandas/commit/8cd8ed3657e52ad9f67e17b7f5c20f7340ab6a2c