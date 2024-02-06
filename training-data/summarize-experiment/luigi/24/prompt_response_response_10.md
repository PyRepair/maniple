Based on the error message and the input parameters, it appears that the issue lies within the `_dict_arg` function where the values from the dictionary are being processed and added to the command list. The discrepancy in the quotation marks around the values in the command list likely stems from the conditional statement in the function. The issue arises when the input dictionary represents a valid configuration for `spark-submit`.

To resolve this issue, the conditional statement in the `_dict_arg` function needs to be corrected in order to properly handle the values from the input dictionary and ensure that they are formatted correctly for the command list.

```python
def _dict_arg(self, name, value):
    command = []
    if value is not None and isinstance(value, dict):
        for prop, val in value.items():
            command += [name, '"{0}={1}"'.format(prop, val)]
    return command
```

By correcting the conditional statement to specifically check for `value is not None` before processing the dictionary items, we ensure that only valid dictionary configurations are processed. This will address the issue of incorrectly formatted values in the command list.

Here is the revised version of the entire `SparkSubmitTask` class with the corrected `_dict_arg` function:

```python
class SparkSubmitTask(luigi.Task):
    """
    Template task for running a Spark job
    
    Supports running jobs on Spark local, standalone, Mesos or Yarn
    
    See http://spark.apache.org/docs/latest/submitting-applications.html
    for more information
    """

    # ... omitted code ...

    def _dict_arg(self, name, value):
        command = []
        if value is not None and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '"{0}={1}"'.format(prop, val)]
        return command
```

By implementing this corrected version, the `_dict_arg` function will handle the input dictionary values appropriately and resolve the issue observed in the test cases.