### Bug Explanation
The bug in the `table_exists` function lies in the comparison check for the presence of the table in the output of the `run_hive_cmd` function. The function is currently checking if the table name is an exact match with the output, which is causing issues due to case sensitivity and potential extra characters (like newline characters) in the output.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison check to account for case insensitivity and ignore any extra characters in the output.

### Corrected Version

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
``` 

In the corrected version:
- I have added `.lower()` to both the table name and the `stdout` output to perform a case-insensitive comparison.
- I replaced the `if stdout: return True else: return False` with `return bool(stdout)` for a clearer and concise logic.