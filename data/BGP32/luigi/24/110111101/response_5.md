## Bug Explanation

The bug lies in how the `command` list is constructed within the `_dict_arg` function. The bug is caused by the incorrect formatting of key-value pairs when creating the command list. In the buggy code, the values are enclosed in double-quotes, whereas they should not be enclosed. This leads to a mismatch between the actual and expected output of the function, causing the tests to fail.

## Bug Fix Strategy

To fix this bug, we need to modify the way key-value pairs are added to the `command` list. Specifically, we should remove the double-quotes around the values before appending them to the list. Additionally, it is important to handle cases where keys or values might contain special characters that could interfere with the formatting.

## Corrected Code

```python
# The relative path of the corrected file: luigi/contrib/spark.py

# The declaration of the class containing the corrected function
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
                command += [name, '{0}={1}'.format(prop, val)]  # Fix: Removed double-quotes from values
        return command
```

By making the above corrections, the `_dict_arg` function will correctly format the key-value pairs without enclosing the values in double-quotes. This change ensures that the function produces the expected output for the test cases provided.