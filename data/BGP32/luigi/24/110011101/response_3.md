### Bug Explanation
The bug in the `_dict_arg` function arises from how it handles the dictionary key-value pairs. The function incorrectly wraps the property-value pair in double quotes, resulting in an incorrect format of the command list. This causes the test cases to fail as the expected command list does not match the actual output due to the presence of double quotes around the property-value pair.

### Bug Fix Strategy
To fix the bug, we need to modify the `_dict_arg` function to correctly format the property-value pairs without enclosing them in double quotes. This can be done by directly appending the property and value to the command list without additional formatting characters.

### Corrected Function
```python
class SparkSubmitTask(luigi.Task):
    """
    Template task for running a Spark job
    
    Supports running jobs on Spark local, standalone, Mesos or Yarn
    
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

By updating the `_dict_arg` function as shown above, we format the property-value pairs correctly without enclosing them in double quotes. This correction should align the actual command list output with the expected values, resolving the failing test cases.