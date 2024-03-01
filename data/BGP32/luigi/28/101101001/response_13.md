### Bug Explanation
The bug in the `table_exists` function is that it incorrectly checks for table existence based on the output of the `run_hive_cmd` function. The function checks if the table name is present in the output, which can lead to false positives if the table name is a substring of another existing table. Additionally, the function does not account for case insensitivity when checking table names.

### Bug Fix Strategy
To fix the bug, we need to modify the `table_exists` function to parse the output from `run_hive_cmd` correctly and perform a case-insensitive check for table existence.

### Corrected Version of the Function
```python
# The relative path of the corrected file: luigi/contrib/hive.py

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        tables = stdout.split()
        return any(tbl.lower() == table.lower() for tbl in tables)
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1};'.format(database, table))

        if stdout:
            return True
        else:
            return False
```

By modifying the function to split the output on whitespace in the case where partition is None and performing a case-insensitive comparison, we can ensure a more accurate check for table existence. This corrected version should now pass the failing test cases.