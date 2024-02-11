The failing test cases suggest that the problem occurs when processing arguments for the Spark submit command, indicating that the issue is most likely with the `_dict_arg` function which is responsible for processing the arguments.

The original error messages are not very descriptive, but it is clear that the failing tests are related to checking the arguments passed to the `proc` when calling the `run` function for `TestSparkSubmitTask` and `TestDefaultSparkSubmitTask`. The `assertEqual` method is used to compare the arguments passed to the `proc`.

Simplified error messages:
1. Original: 
   AssertionError: Lists differ: ['ss-[240 chars]f', '"Prop=Value"', ...] != ['ss-[240 chars]f', 'Prop=Value', ...]
   First differing element 18: '"Prop=Value"' vs 'Prop=Value'

2. Original:
   AssertionError: Lists differ: ['ss-[131 chars] '--archives', 'archive1', '--conf, ...'] != ['ss-[131 chars] '--archives', 'archive1', '--conf', 'prop1=val1', 'test.py']
   First differing element 12: '"prop1=val1"' vs 'prop1=val1'

By simplifying the messages, we can identify that the error is likely caused by the way values are being processed or formatted in the `_dict_arg` function. The "prop1=val1" appears to be the key-value switch and arguments are enclosed within quotes incorrectly which causes the comparison to fail, and provokes the error message.

The fix will be to modify the `_dict_arg` function to handle the key-value switches and arguments correctly and to ensure proper formatting in the function.