### Bug Explanation
The bug in the `_dict_arg` function stems from the fact that it appends the dictionary values to the `command` list incorrectly. It wraps the property and value inside double quotes, but it should not be enclosed in quotes.

### Solution Strategy
To fix the bug, we need to remove the double quotes around the property and value when appending them to the `command` list.

### Corrected Version
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

By making this change, the corrected function will correctly format the property and value pairs when generating the command list, ensuring it aligns with the expected values and passing the failing tests.