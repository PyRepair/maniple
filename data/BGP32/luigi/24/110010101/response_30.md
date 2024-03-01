### Analysis
The buggy function `_dict_arg` is intended to convert a dictionary into a list of command-line arguments. The issue is with how it handles the dictionary values. The function currently wraps the values in double quotes, which is incorrect for command-line arguments.

#### Bug Cause
The bug occurs because the function incorrectly wraps the property values in double quotes before appending them to the command list. The test cases expect the values not to be wrapped in double quotes.

#### Fix Strategy
To fix the bug, we need to modify the way the property values are appended to the command list. We should add the property name and value directly to the list without wrapping the value in double quotes.

### Code Correction

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

By making this change, the function will correctly generate the list of command-line arguments without wrapping the values in double quotes. This correction should pass the failing test cases with the expected input/output values.