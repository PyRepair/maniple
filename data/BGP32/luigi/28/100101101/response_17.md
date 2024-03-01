### Bug Explanation
The bug in the `table_exists` function lies in the comparison between the expected table name and the output obtained from the `run_hive_cmd` function. The buggy function checks if the table name is in the output string received from the `run_hive_cmd` function. However, this check is not done correctly as it does not account for potential whitespace or formatting issues in the output string.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison method to ensure that the table name is extracted correctly from the output string and matched against the expected table name. We should also consider case insensitivity to handle different cases of table names.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))

        return stdout and table.lower() in stdout.lower().split()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```  

### Correction Explanation
- Modified the query in the `stdout` assignment to properly show tables in the specific database.
- Adjusted the comparison to check if the lowercase version of the expected table name is in the lowercase version of the output tables after splitting. This handles potential casing discrepancies.
- Added the `.split()` method to separate the tables in the output string for a more accurate comparison.