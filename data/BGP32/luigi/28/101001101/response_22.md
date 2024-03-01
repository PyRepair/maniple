### Bug Explanation
The bug in the `table_exists` function lies in the condition that checks if the table exists in the output of the `run_hive_cmd` function. The bug occurs because the function doesn't handle the case where the table name in the output of `run_hive_cmd` matches another table name partially. For example, in Case 2, the function incorrectly identifies `'mytable'` as part of the output `'OK\nmytable'`, leading to a false positive result.

### Bug Fix Strategy
To fix the bug, we need to improve the condition that checks if the table name exists in the output of `run_hive_cmd` more rigorously. We should match the table name as a whole to avoid false positives. Additionally, we need to account for case sensitivity in table names to ensure accurate results.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                          (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version, we convert both the table name being checked and the names within the output to lowercase before comparing to ensure case insensitivity. This approach prevents false positives due to partial matches.