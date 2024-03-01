### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the existence of the table. In both cases where `stdout` is checked for truthiness (`if stdout:`), the return values are incorrectly handled. The function does not correctly check if the table exists in the output of the Hive command after querying. 

1. In the first case, the function checks if the table name is directly present in the `stdout` output, which is incorrect because the table name could be part of a larger string.
2. In the second case, the function simply checks if the `stdout` exists, which does not guarantee that the table actually exists in the output.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the function to extract the table names from the `stdout` output correctly and then check if the specified table exists within those extracted table names.

### Corrected Version of the Function
```python
# The relative path of the corrected file: luigi/contrib/hive.py

from luigi.contrib.hive import HiveClient, run_hive_cmd

class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
            tables = stdout.split()
            return table in tables
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

In the corrected version of the function:
- In the first case, `stdout` is split into separate table names, and then the function checks if the specified table name exists in those extracted table names.
- In the second case, the function explicitly checks if `stdout` has any value, returning `True` if it does.