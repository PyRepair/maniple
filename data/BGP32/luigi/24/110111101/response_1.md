## Bug Explanation
The bug in the `_dict_arg` function is caused by the way the values are being concatenated to form the `command` list. The current implementation adds unnecessary double quotes around the property-value pairs when constructing the command list, leading to a mismatch in the expected and actual outputs.

## Bug Fix Strategy
To fix the bug, we need to modify how the property-value pairs are formatted and added to the `command` list. We should concatenate the property and value directly without enclosing them in double quotes.

## Corrected Version of the Function
Here is the corrected version of the `_dict_arg` function:

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

    # Corrected version of the buggy function
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '{0}={1}'.format(prop, val)]
        return command
```

By making this change, the corrected function should now properly construct the command list without unnecessary double quotes around property-value pairs as in the original buggy version. This modification should address the issues causing the failing tests.