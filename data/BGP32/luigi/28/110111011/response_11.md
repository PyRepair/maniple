There are two main issues causing the failing test cases:

1. The `table_exists` function is case-sensitive, causing the test cases with mixed-case table names to fail.
   
2. The function does not handle multiple table names separated by newline characters (e.g., "OK\nmytable") correctly.

To fix these issues, we need to modify the `table_exists` function to ensure case insensitivity when comparing table names and handle multiple table names appropriately.

Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """
    
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables;'.format(database))
            tables = stdout.split('\n')
            return any(table.lower() == t.lower() for t in tables)

        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

By splitting the stdout into individual tables in the modified function, we can compare each table name with the desired table name in a case-insensitive manner. This change will address the case sensitivity issue as reported in the GitHub issue (#896).

With this corrected version, the failing test cases should pass without any issues related to table name cases or multiple table names returned.