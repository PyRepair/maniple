The bug in the provided function is related to the condition checking for the existence of a table in a database. The bug is in the way the function checks for the table existence based on the stdout returned from the `run_hive_cmd` function.

The bug occurs due to the incorrect check of whether the table name is in the stdout. In the first case, the stdout might contain other tables' names along with the table being checked, leading to a false positive result. 

To fix the bug, we should modify the function to split the stdout by newlines and then check if the exact table name is present in the list of tables.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        table_list = stdout.split('\n')
        return table in table_list
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

This correction ensures that the function accurately checks if the provided table name is existent in the list of tables returned by the Hive command.

The corrected version should now correctly handle the cases mentioned and provide the expected output.