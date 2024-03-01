### Bug Explanation
The bug in the `table_exists` function arises from how the function processes the `stdout` variable to determine if a table exists. The function currently checks whether the table name is within the `stdout` variable as a substring, which is causing incorrect outputs for certain cases due to the way `stdout` is constructed.

Specifically, the issue comes from how the function constructs the `stdout` variable when calling `run_hive_cmd` and processes it in the `if` condition. In Case 2, for instance, the `stdout` is `'OK\nmytable'`, causing the function to mistakenly identify the table as existing due to the presence of the string `'mytable'`.

### Fix Strategy
To fix the bug, we need to modify the logic in the `if` condition where the function checks for the table's existence. Instead of simply checking if the table name is present in `stdout`, we should split `stdout` correctly based on the expected format.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout.split()

        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)

```