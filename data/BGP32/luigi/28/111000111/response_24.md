The buggy function `table_exists` is currently case-sensitive when checking for the existence of a table in Hive. The issue reported on GitHub highlights the need to make this function case-insensitive to handle different naming conventions efficiently.

### Error Location:
The bug arises in the function's comparison of the `table` name with the tables retrieved from Hive. The comparison is sensitive to the case of the table names, leading to false negatives when encountering tables with different case styles.

### Bug Cause:
The bug stems from the function's logic in checking for table existence. When retrieving table names from Hive, these names might not match the provided `table` parameter due to differences in case. This discrepancy results in the function incorrectly determining the existence of a table.

### Strategy for Bug Fix:
To resolve the bug, the function needs to compare the lowercase version of the provided `table` name with the lowercase table names retrieved from Hive. This adjustment ensures a case-insensitive comparison and guarantees accurate table existence checking.

### Corrected Function:
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

By modifying the function to compare lowercase versions of table names, the corrected version now ensures a case-insensitive approach to determining the existence of tables in Hive. This enhancement aligns with the GitHub issue's suggestion and resolves the reported bug effectively.