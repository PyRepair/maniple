The issue in the code is that the assertion `assert len(input_shape) == 2` fails because `input_shape` is a tuple with a length of 3 instead of 2.

To fix