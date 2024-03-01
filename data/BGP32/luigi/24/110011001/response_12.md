### Bug Analysis
1. The function `_dict_arg` is intended to create a list of arguments for a command based on a dictionary provided as input.
2. The bug occurs because the function is adding extra quotes around the value part when it should not.
3. In Case 1, the function outputs `'"Prop=Value"'` instead of simply `'Prop=Value'`, causing the test to fail due to the mismatch in the expected and actual values.
4. In Case 2, a similar issue happens where `'"prop1=val1"'` is generated instead of `'prop1=val1'`.
5. The incorrect format of the values is causing the assertion errors in the tests.

### Bug Fix Strategy
To fix the bug, we need to modify the function so that it correctly adds the argument without extra quotes around the value. This can be done by removing the additional quotes when formatting the argument string.

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

By modifying the function as shown above, the extra quotes issue should be resolved, and the corrected version should pass the failing tests.