### Explanation:
The bug in the `table_exists` function lies in the condition for checking if the table exists in the output of the `run_hive_cmd` function. The function incorrectly checks for the presence of the table name in the output, causing the tests to fail.

1. In cases where the table name is alone in the output (e.g., "OK\nmytable"), the function incorrectly returns False because it assumes that the table is not present if it doesn't have any additional information.
2. In cases where the table name is followed by other information (e.g., "OK\nmytable"), the function incorrectly returns True even though the additional information is not relevant to determining the existence of the table.

### Strategy for fixing the bug:
To fix the bug, the function should check if the exact table name is present in the output from `run_hive_cmd`. If the table name is present and is not part of another string, the function should return True; otherwise, it should return False.

Let's modify the function to handle this case correctly.

### Corrected Version:

```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return table in stdout.split('\n')

        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

By splitting the stdout by newline character and checking if the table name is present in the resulting list, we ensure that the function correctly detects the presence of the table in the output. This fix should make the tests pass as expected.