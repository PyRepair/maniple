## Bug Analysis:
The bug in the `table_exists` function lies in the conditional check where the function tries to validate if the table exists based on the output received from `run_hive_cmd`. The issue arises from the fact that when checking if a table exists without partitions, the function is using index logic where it should be using `in`. Additionally, in cases where partitions are involved, the formatting of the query is incorrect.

## Bug Fix Strategy:
1. Update the conditional statements to correctly check for the existence of tables in both cases.
2. Correct the formatting of the query when dealing with partitions.

## Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                                ({2})""".format(database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
``` 

After applying these fixes, the function should now pass all the expected test cases provided and correctly determine the existence of tables both with and without partitions.