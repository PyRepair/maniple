## Bug Analysis
The bug in the `table_exists` function lies in the conditional check for the existence of the table. The function checks if the `table` string is in the output of the `run_hive_cmd` function, which may lead to false positives due to substring matches. This causes the failing tests to incorrectly return `False` when the table actually exists.

## Bug Explanation
1. In Case 1 and Case 3, the function is returning `False` when the table is present because the `stdout` variable contains the substring `'OK'` which causes the conditional check `table in stdout` to fail.

2. In Case 2 and Case 4, the function correctly identifies the table in the `stdout`, but the use of substring matching causes false positives.

## Bug Fix Strategy
To fix the bug, we should modify the condition to check for exact matches between the `table` name and the entries in the `stdout`. This ensures that only exact table names are considered, avoiding false positives from substring matches.

## Corrected Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                          (%s)""" % (database, table, self.partition_spec(partition)))
        return True if stdout else False
``` 

With this modification, the function splits the `stdout` by newlines and checks for an exact match between the `table` name and each entry in the result. This corrected approach ensures that the function correctly identifies the presence of the table without relying on problematic substring checks.