Here is the corrected version of the function:

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
            for prop, val in value.items():  # Change the variable name from value to val
                command += [name, '--{0}={1}'.format(prop, val)]  # Change the string format and remove unnecessary quotes
        return command
```

In this corrected version, the function now correctly iterates through the key-value pairs of the input dictionary and appends them to the command list in the format "--name=value". The unnecessary quotes around the value have been removed, and the variable name inside the for loop has been changed to avoid confusion with the outer 'value' variable.

This corrected version should now pass the failing test cases and produce the expected output.