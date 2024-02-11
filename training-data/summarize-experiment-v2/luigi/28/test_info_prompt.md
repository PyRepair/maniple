Please analyze the provided error message on command line, test code, and buggy source code, then identify what stack frames or messages are closely related to the fault location and simplify the original error message.


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/hive.py



    # this is the buggy function you need to fix
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
    
```


# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

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


# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_apacheclient_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.apacheclient.table_exists("mytable")
        self.assertFalse(returned)

        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.apacheclient.table_exists("mytable")
        self.assertTrue(returned)

        # Issue #896 test case insensitivity
        returned = self.apacheclient.table_exists("MyTable")
        self.assertTrue(returned)

        run_command.return_value = "day=2013-06-28/hour=3\n" \
                                   "day=2013-06-28/hour=4\n" \
                                   "day=2013-07-07/hour=2\n"
        self.apacheclient.partition_spec = mock.Mock(name="partition_spec")
        self.apacheclient.partition_spec.return_value = "somepart"
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertTrue(returned)

        run_command.return_value = ""
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertFalse(returned)
```


## The error message from the failing test
```text
self = <contrib.hive_test.HiveCommandClientTest testMethod=test_table_exists>
run_command = <MagicMock name='run_hive_cmd' id='140453047166864'>

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
>       self.assertTrue(returned)
E       AssertionError: False is not true

test/contrib/hive_test.py:111: AssertionError

```
## The error message from the failing test
```text
self = <contrib.hive_test.HiveCommandClientTest testMethod=test_apacheclient_table_exists>
run_command = <MagicMock name='run_hive_cmd' id='140453047093088'>

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_apacheclient_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.apacheclient.table_exists("mytable")
        self.assertFalse(returned)
    
        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.apacheclient.table_exists("mytable")
        self.assertTrue(returned)
    
        # Issue #896 test case insensitivity
        returned = self.apacheclient.table_exists("MyTable")
>       self.assertTrue(returned)
E       AssertionError: False is not true

test/contrib/hive_test.py:175: AssertionError

```