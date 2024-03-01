### Bug Explanation
The bug in the `_dict_arg` function arises from the way it constructs the command list when the input value is a dictionary. The function incorrectly adds quotation marks around the property value pairs when creating the command list, resulting in a mismatch in the expected and actual command lists during testing.

### Bug Fix Strategy
To fix the bug, we need to modify the `_dict_arg` function to correctly construct the command list without adding unnecessary quotation marks around property value pairs.

### Corrected Version of the Function
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

By making this modification, the corrected `_dict_arg` function will now properly construct the command list without including extra quotation marks around property value pairs, resolving the issues observed during testing.