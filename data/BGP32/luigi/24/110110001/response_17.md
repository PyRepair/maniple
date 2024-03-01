### Analysis:
1. The function `_dict_arg` in the class `SparkSubmitTask` is supposed to convert a dictionary into a list of command-line arguments.
2. The function currently wraps the values in the dictionary with extra double quotes causing discrepancies in the test cases.
3. The failing test cases check the generated command against an expected command, and the failing occurs due to extra double quotes added during the conversion process.
4. To fix the bug, we need to modify the `_dict_arg` function to format the arguments correctly without adding extra double quotes.

### Bug Fix:
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
                command += [name, '{}={}'.format(prop, val)]
        return command
```

This fix involves changing the format method to `{}` instead of `"{0}={1}"` to remove the unnecessary double quotes. This updated version should pass the provided failing test cases.