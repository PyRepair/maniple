### Bug Explanation

The bug in the `table_exists` function is due to the comparison check for the existence of the table. When checking for the table's existence based on the output of the `run_hive_cmd` function, the code is only checking if the table name is present in the stdout, which can lead to incorrect results.

In the failing test cases provided:
- Case 1 and Case 3: The return value of `run_hive_cmd` is `'OK'`. The code checks if the table name is in the stdout, which is true for 'mytable', resulting in an incorrect `True` return value.
- Case 2 and Case 4: The return value of `run_hive_cmd` contains `'OK\nmytable'`. The code again checks if the table name is in the stdout, resulting in an incorrect `False` return value, even though the table 'MyTable' is present.

### Bug Fix Strategy

To fix the bug, we need to modify the comparison check in the `table_exists` function. Instead of checking if the table name is directly in the stdout, we should parse the output properly and verify the existence of the table in a more reliable manner.

### Corrected Version

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            
            # Modify the comparison check to properly parse the stdout
            return stdout and table in stdout.split()

        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            
            # Modify the check for the existence of the table in parsed output
            return 'OK' in stdout.split()

```