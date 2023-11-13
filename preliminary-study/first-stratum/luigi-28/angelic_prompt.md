You have a snippet filling problem. Consider the code snippet:
    
The buggy code is:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        <MISSING_SNIPPET>
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```
    
The test function is:

```python
@mock.patch("luigi.contrib.hive.run_hive_cmd")
def test_table_exists(self, run_command):
    run_command.return_value = "OK"
    returned = self.client.table_exists("mytable")
    self.assertFalse(returned)

    run_command.return_value = "OK\n" \
                                "mytable"
    returned = self.client.table_exists("mytable")
    self.assertTrue(returned)

    # Issue #896 test case insensitivity
    returned = self.client.table_exists("MyTable")
    self.assertTrue(returned)

    run_command.return_value = "day=2013-06-28/hour=3\n" \
                                "day=2013-06-28/hour=4\n" \
                                "day=2013-07-07/hour=2\n"
    self.client.partition_spec = mock.Mock(name="partition_spec")
    self.client.partition_spec.return_value = "somepart"
    returned = self.client.table_exists("mytable", partition={'a': 'b'})
    self.assertTrue(returned)

    run_command.return_value = ""
    returned = self.client.table_exists("mytable", partition={'a': 'b'})
    self.assertFalse(returned)
```

The values of variables before the snippet: (TEST CASE 1)
database: "default", partition: None, stdout: "OK", table: "mytable"
The expected values of variables after the snippet:
returned: False

The values of variables before the snippet: (TEST CASE 2)
database: "default", partition: None, stdout: 'OK\nmytable', table: "mytable"
The expected values of variables after the snippet:
returned: True

The values of variables before the snippet: (TEST CASE 3)
database: "default", partition: None, stdout: 'OK\nmytable', table: "MyTable"
The values of variables before the snippet: (TEST CASE 3)
returned: True
