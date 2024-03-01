### Bug Explanation:
The bug in the `table_exists` function lies in the conditional check for the presence of the table name in the `stdout` response from the `run_hive_cmd` function. The issue arises because the buggy code checks if the `table` name is in the `stdout` directly without considering the formatting of the `stdout` response. 

In the failing test case where `table_exists("MyTable")` is called, the expected `stdout` response is `"OK\nmytable"`. However, the buggy code checks for the exact matching of `table` in the `stdout`, leading to a false assertion error.

### Bug Fix Strategy:
1. Modify the condition that checks for the presence of the table name in `stdout` to handle cases where the table name might be a substring of a larger string (like in the case of multiline `stdout` responses).
2. Update the comparison logic to check if the `table` name appears as a separate word in the `stdout`.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return any(line.strip() == table for line in stdout.splitlines())
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` response into lines and checking if the table name exactly matches any line in the response, we ensure that the function can correctly identify the presence of the table name in the output, fixing the bug.