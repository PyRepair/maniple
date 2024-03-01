### Bug Explanation:
The bug in the `table_exists` function stems from the fact that the comparison between the table name and the table names in the stdout returned by the `run_hive_cmd` function is case-sensitive. Since Hive is case-insensitive, the table names might be returned in a different casing than provided, leading to failing tests when comparing the exact string.

### Bug Fix Strategy:
To fix the bug, we need to make the comparison case-insensitive by converting both the table name and the table names in the stdout to lowercase before the comparison. This approach will align with the expected behavior of Hive and address the failing tests due to case sensitivity.

### Corrected Function:
Here is the corrected version of the `table_exists` function:

```python
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

By converting both the table name and the stdout to lowercase before comparison, the `table_exists` function becomes case-insensitive, addressing the issue reported in the failing tests.