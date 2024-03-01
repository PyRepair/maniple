### Bug Explanation
The bug in the `_dict_arg` function arises from the incorrect handling of dictionary values when constructing the command list. The function incorrectly wraps the property values in double quotes, causing the final command list to contain incorrectly formatted elements when compared to the expected output in the test cases.

In Case 1, the property `"Prop=Value"` is enclosed in double quotes, resulting in a mismatch with the expected value of `'Prop=Value'`. This discrepancy causes the assertion error in the test.

In Case 2, a similar issue occurs with the property `'prop1=val1'`, where the function erroneously adds double quotes around the value.

### Bug Fix Strategy
To fix the bug, the function `_dict_arg` should avoid wrapping the property values in double quotes before appending them to the command list. This adjustment will ensure that the generated command list matches the expected format in the test cases.

### Corrected Version of the `_dict_arg` Function
```python
class SparkSubmitTask(luigi.Task):
    """
    Template task for running a Spark job
    
    Supports running jobs on Spark local, standalone, Mesos, or Yarn
    
    See http://spark.apache.org/docs/latest/submitting-applications.html
    for more information
    """


    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '{0}={1}'.format(prop, val)]
        return command
```

By revising the `_dict_arg` function as shown above, the properties and values will be correctly formatted without unnecessary quotes, resolving the issues observed in the failing test cases.