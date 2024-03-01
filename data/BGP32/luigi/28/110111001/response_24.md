### Bug Explanation:
The bug in the `table_exists` function lies in the condition where the function checks if the table is present in the `stdout` returned from the `run_hive_cmd`. The function compares the table name directly with the `stdout`, which can cause unexpected behavior due to potential extra characters, newlines, or other formatting issues in the `stdout`.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic for checking the existence of the table in the `stdout`. Instead of checking if the table name is directly in the `stdout`, we should parse the `stdout` correctly to extract the table names and then check if the desired table is present in those names.

### Corrected Version of the `table_exists` function:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            tables = stdout.split('\n')[1:]  # Skip the header
            return table in tables
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

By splitting the `stdout` by newline characters and extracting the table names properly, we ensure that we are correctly checking the existence of the table in the list of table names returned. This approach will address the bug and make the function behave as expected.