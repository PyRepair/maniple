### Bug Explanation
The bug in the `table_exists` function arises from the incorrect logic in checking for the presence of a table or partition in the Hive database. 

In the `if partition is None:` block, the function constructs a query to check for the existence of a table in the specified database but incorrectly checks if the table name is contained in the entire `stdout` output string, leading to false negatives.

In the `else:` block, when checking for the existence of a partition in a table, the function constructs the query correctly but incorrectly checks only for the presence of any output, which leads to erroneous results.

### Fix Strategy
To fix the bug, we need to modify the function to correctly parse the output from the Hive commands and appropriately check for the existence of tables and partitions.

Firstly, in the `if partition is None:` block, we will split the `stdout` by newline characters and then check if the table name appears in any line of the output.

Secondly, in the `else:` block, we will modify the condition to check if the number of partitions returned is greater than 0 to confirm the existence of the specified partition.

### Corrected Version

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return any(table == line.strip() for line in stdout.split('\n'))
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            return len(stdout.strip().split('\n')) > 0
``` 

The corrected function should now properly check for the existence of tables and partitions in the Hive database based on the given input parameters.