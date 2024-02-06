The bug in the `table_exists` function originates from the incorrect handling of the `stdout` variable and the table name comparison. The `table_exists` function should accurately determine the existence of a table in a specified database and partition. 

The buggy function incorrectly handles the case where `stdout` is "OK" but the table doesn't exist, leading to an incorrect return value. The function also fails to properly handle partitioned tables, always returning `True` regardless of the actual outcome of the hive command.

To fix the bug, the condition for checking the existence of the table needs to be revised to handle cases where the table doesn't exist and to accurately determine the existence in both cases with and without partition. Additionally, the function should be made case-insensitive.

Based on the test cases and error messages, the following corrected code for the `table_exists` function is provided below. The fixes are implemented by adjusting the conditions and making the comparison case-insensitive.

```python
class HiveCommandClient(HiveClient):
    # ... (omitted code)

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            if stdout:
                return True
            else:
                return False
```

The revised version of the `table_exists` function addresses the bugs by making the comparison case-insensitive and correctly determining the existence of the table in both cases with and without partition. This corrected code can be used as a drop-in replacement for the buggy version of the function.