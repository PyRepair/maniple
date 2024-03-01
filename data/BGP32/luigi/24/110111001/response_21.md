### Bug Explanation
The bug in the `_dict_arg` function is caused by the incorrect handling of dictionary values when constructing the `command` list. The function incorrectly adds double quotes around the value part of each key-value pair in the dictionary, which leads to a mismatch with the expected argument format in the test cases.

In the failing tests, the function is expected to generate command arguments like `--conf prop1=val1`, but instead, it generates `--conf "prop1=val1"`, which causes the assertion errors.

### Bug Fix Strategy
To fix the bug, we need to modify the `_dict_arg` function to correctly construct the command list without adding unnecessary double quotes around the dictionary values. This can be achieved by directly concatenating the key-value pair strings without quotes.

### Corrected Version
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

By removing the unnecessary double quotes around the dictionary values, the corrected version of the `_dict_arg` function should now generate the correct command arguments and pass the failing tests.