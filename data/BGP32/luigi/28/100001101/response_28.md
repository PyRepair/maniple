## Bugs identified:
1. The function does not correctly check for table existence in the database.
2. The function does not handle the case-insensitive nature of table names in Hive.
3. The function does not handle the partition parameter correctly.

## Bug fixes and explanations:
1. Modify the function to check for table existence using a case-insensitive comparison.
2. Update the function to handle the partition parameter properly.

## Corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                        ({2});""".format(database, table, self.partition_spec(partition)))

        return bool(stdout)
```