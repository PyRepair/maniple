### Bug Explanation:
The bug in the `table_exists` function lies in the logic when checking the existence of a table. The function is incorrectly checking for the presence of the table name in the output of the `run_hive_cmd` function, which can lead to false positives or false negatives due to the simplistic string comparison approach.

### Bug in `table_exists` function:
1. In the `if partition is None` block, the function checks if the table name is `in stdout`, which can lead to incorrect results, as the table name might exist as a substring in the output.
2. In the `else` block, the function simply checks for the existence of any output from the `run_hive_cmd` function, which is not a reliable way to determine table existence.

### Bug Fix Strategy:
To fix the bug in the `table_exists` function, we need to modify the logic of how table existence is checked. Instead of relying on string containment within command output, we should parse the output more accurately and check for the presence of the exact table name.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return table in stdout.split('\n')  # Exact match check 
        else:
            return False
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the output by line breaks and checking for an exact match with the table name, we can ensure more accurate table existence checks.