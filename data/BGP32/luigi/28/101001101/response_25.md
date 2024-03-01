### Bug Analysis:
The bug in the `table_exists` function lies in the logic of checking if the table exists in the database. In the case where no partition is specified, the function incorrectly checks if the entire `table` string is present in the `stdout` instead of checking if a row containing the table name exists. In the case where a partition is specified, the function queries for partitions based on the `partition_spec` function but does not properly handle the output to determine if the table exists.

### Bug Fix Strategy:
1. In the case where no partition is specified, check if the `table` is present in any row of the `stdout` instead of just checking for an exact match.
2. In the case where a partition is specified, verify if the output contains the partitions using `self.partition_spec` to confirm the table's existence.

### Corrected Code:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        return any(table == t for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partition %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        return bool(partitions)
``` 

The corrected code adjusts the logic in each case to properly check for the existence of the table based on the queried output, whether partitions are specified or not.