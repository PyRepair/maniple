### Bug Explanation:
The bug in the `table_exists` function lies in how it checks the existence of a table. In the first part of the function, it checks if the table name is present in the output of the `run_hive_cmd` function, which may lead to false positives if the table name is a substring of another table name in the output. This causes the failing test cases where the function incorrectly returns `False` when it is expected to return `True`.

### Bug Fix Strategy:
To fix the bug, we need to modify how we check the existence of the table. Instead of simply checking if the table name is present in the output, we should ensure that the table name is a separate entry in the output to prevent false positives.

### Updated Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
    
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

### Changes Made:
1. In the first part, instead of checking if the table name is in the output directly, we split the output by lines and then check if the table name is one of the entries. This prevents false positives.
2. In the second part, we directly convert the stdout to a boolean value to check if any partitions are returned.

By making these changes, the function should now correctly identify the existence of the table and pass the failing test cases.