### Bug Explanation
The bug occurs because the `table_exists` function is incorrectly implemented to return `True` only if the output of the `run_hive_cmd` is not empty. In both failing test cases, the function fails to check whether the table name is present in the output correctly. This results in incorrect evaluation of whether the table exists or not.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison of the table name in the output of `run_hive_cmd` to determine if the table exists. The function should check if the table name appears in the output, regardless of whether there are other contents present.

### Corrected Function

```python
# The relative path of the corrected file: luigi/contrib/hive.py

# The corrected version of the class containing the buggy function
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout is not None and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            return table in stdout if stdout else False
```

By implementing the corrected function above, we ensure that the function checks if the table name is present in the output of `run_hive_cmd` to accurately determine if the table exists, instead of solely relying on the presence or absence of output. This modification should resolve the issue and make the function behave as expected in all the test cases.