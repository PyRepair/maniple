The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi.contrib.hive` module has a bug where it fails to be case insensitive when checking for the existence of a table, causing tests to fail. The issue is related to GitHub issue #896, which suggests making the `table_exists` function case insensitive.

### Bug Analysis:
- The function `table_exists` checks if a table exists in Hive by running a Hive command and comparing the output with the table name.
- The bug occurs because the comparison against the table name is case-sensitive, leading to test failures when the case mismatches.

### Bug Location:
The bug is located in the following code snippet:
```python
return stdout and table in stdout
```

### Bug Explanation:
- In the failing test cases, the expected table names are provided with various cases (e.g., 'mytable', 'MyTable').
- The buggy function directly checks if the table name is in the output string without considering case sensitivity.
- When the table name in the output string doesn't match the case of the provided table name, the comparison fails, leading to incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to make the comparison case insensitive by converting both the table name and the output string to lowercase before comparing them.

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
    
        return bool(stdout)
```

By converting both the table name and the output string to lowercase during the comparison, the corrected function will now be case insensitive when checking for the existence of a table in Hive.

The corrected function should now pass all the failing test cases while satisfying the expected input/output values and resolving the issue raised on GitHub.