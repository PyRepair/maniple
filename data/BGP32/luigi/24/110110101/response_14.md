### Analysis:
1. The `SparkSubmitTask` class contains a `_dict_arg` method which is intended to convert a dictionary into a list of command arguments.
2. The bug in the `_dict_arg` method is that it adds double quotes around the property=value pairs, which is causing the test cases to fail.
3. The failing tests provide dictionaries with properties and values, but the buggy function is converting them incorrectly by adding extra double quotes.
4. To fix the bug, we need to remove the unnecessary double quotes around the property=value pairs in the command list.
5. The corrected version of the `_dict_arg` method is provided below.

### Corrected Version:
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

With this correction, the `TestSparkSubmitTask` and `TestDefaultSparkSubmitTask` test cases should pass successfully.