### Bug Explanation
The root cause of the bug is that the `_dict_arg` function is incorrectly processing dictionary values. When preparing the command list, it wraps the values of the dictionary in double quotes, which leads to a discrepancy between the expected and actual values. The expected values are without quotes, while the actual values include quotes due to the formatting.

### Bug Fix Strategy
To fix this bug, we need to modify how the values from the dictionary are added to the command list. Instead of including them in double quotes, we should directly append them in the format `key=value`.

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

    # Corrected version of the buggy function
    def _dict_arg(self, name, value):
        command = []
        if value and isinstance(value, dict):
            for prop, val in value.items():
                command += [name, '{0}={1}'.format(prop, val)]
        return command
```

After applying this correction, the function should correctly format the commands without unnecessary double quotes, aligning with the expected values provided.