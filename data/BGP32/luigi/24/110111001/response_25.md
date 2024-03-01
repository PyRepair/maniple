### Bug Explanation
The bug in the `_dict_arg` function stems from incorrect handling of the dictionary values when constructing the command list. The function mistakenly wraps the property-value pairs in double quotes, causing a mismatch in the expected and actual command arguments.

### Bug Fix Strategy
To fix the bug, we need to adjust how the property-value pairs are added to the command list. Instead of wrapping the pairs with double quotes, we should append them directly without quotes.

### Corrected Version of the Function
```python
# The relative path of the buggy file: luigi/contrib/spark.py

# The declaration of the class containing the buggy function
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
            for prop, val in value.items():  # renaming value to val to avoid conflict with value parameter
                command += [name, '{0}={1}'.format(prop, val)]  # corrected formatting
        return command
```

By correcting the `_dict_arg` function as described above, it should now properly construct the command list without unnecessary double quotes, addressing the issue and allowing the failing tests to pass.