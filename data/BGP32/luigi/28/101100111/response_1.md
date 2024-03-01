### Analysis:
1. The buggy function `table_exists` in the `HiveCommandClient` class is supposed to check if a table exists in the specified database. However, there is a case sensitivity issue where the function does not handle table names in a case-insensitive manner.
2. The function calls the `run_hive_cmd` function to execute a Hive command and check the output for the existence of the table.
3. The bug arises from not performing a case-insensitive comparison between the table name and the output from the `run_hive_cmd` function.
4. To fix the bug, we need to convert both the table name and the output to lowercase for comparison.

### Bug Fix Strategy:
1. Modify the `table_exists` function to convert both the table name and the `stdout` output to lowercase before comparison.
2. Update the function to handle case sensitivity properly by making a case-insensitive comparison.
3. Implement the changes based on the expected input/output values and the identified bug.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
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

The corrected version of the `table_exists` function now converts both the table name and the output to lowercase before comparing them, ensuring a case-insensitive check for table existence.

This fix should resolve the case sensitivity issue reported in the GitHub issue #896.