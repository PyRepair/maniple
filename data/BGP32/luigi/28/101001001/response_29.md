### Bug Explanation
The bug in the `table_exists` function is related to how the function checks for the existence of a table in Hive. In the `if partition is None` branch, the function correctly executes a Hive command to check for the table existence based on the provided `table` and `database`. However, in the `else` branch where a partition is provided, the function constructs a Hive command to show partitions for the specified `table` and `partition`. The issue arises from comparing the output of these Hive commands to determine if the table exists.

The current implementation checks if the output string is not empty (`stdout`) to determine if the table exists. This leads to incorrect results because the `stdout` variable may contain other information from the Hive command other than just the existence of the table.

### Bug Fix Strategy
To fix this bug, we need to modify the way we check for the existence of the table based on the output of the Hive commands. We should parse the output of the Hive commands to extract the information about the table existence accurately.

### Corrected Version of the Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        return any(table.lower() == t.lower() for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = stdout.split('\n')
        return any(partition.lower() == p.lower() for p in partitions)
```

In the corrected version, we split the `stdout` string based on newlines and compare each line with the provided `table` or `partition` (case insensitive comparison) to accurately determine if the table or partition exists. This approach ensures that we are checking the expected information from the Hive commands' output.