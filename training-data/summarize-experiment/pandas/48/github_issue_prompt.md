You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
calling mean on a DataFrameGroupBy with Int64 dtype results in TypeError
```

## The associated detailed issue description
```text
import pandas as pd

df = pd.DataFrame({
    'a' : [0,0,1,1,2,2,3,3],
    'b' : [1,2,3,4,5,6,7,8]
},
dtype='Int64')

df.groupby('a').mean()

Problem description
Using the new nullable integer data type, calling mean after grouping results in a TypeError. Using int64 dtype it works:
import pandas as pd

df = pd.DataFrame({
    'a' : [0,0,1,1,2,2,3,3],
    'b' : [1,2,3,4,5,6,7,8]
},
dtype='int64')

print(df.groupby('a').mean())

as does keeping Int64 dtype but taking a single column to give a SeriesGroupBy:
import pandas as pd

df = pd.DataFrame({
    'a' : [0,0,1,1,2,2,3,3],
    'b' : [1,2,3,4,5,6,7,8]
},
dtype='Int64')

print(df.groupby('a')['b'].mean())

The error does not occur when calling min, max or first, but does also occur with median and std.
Expected Output
     b
a     
0  1.5
1  3.5
2  5.5
3  7.5

Output of pd.show_versions()
[paste the output of pd.show_versions() here below this line]
INSTALLED VERSIONS
commit : None
python : 3.7.3.final.0
python-bits : 64
OS : Linux
OS-release : 4.15.0-74-generic
machine : x86_64
processor : x86_64
byteorder : little
LC_ALL : None
LANG : en_GB.UTF-8
LOCALE : en_GB.UTF-8

pandas : 1.0.1
numpy : 1.18.1
pytz : 2019.1
dateutil : 2.8.0
pip : 19.1.1
setuptools : 41.0.1
Cython : None
pytest : 5.3.4
hypothesis : None
sphinx : None
blosc : None
feather : None
xlsxwriter : None
lxml.etree : 4.3.3
html5lib : None
pymysql : None
psycopg2 : None
jinja2 : 2.10.1
IPython : 7.5.0
pandas_datareader: None
bs4 : 4.8.1
bottleneck : None
fastparquet : None
gcsfs : None
lxml.etree : 4.3.3
matplotlib : 3.1.2
numexpr : None
odfpy : None
openpyxl : None
pandas_gbq : None
pyarrow : None
pytables : None
pytest : 5.3.4
pyxlsb : None
s3fs : None
scipy : 1.3.0
sqlalchemy : None
tables : None
tabulate : None
xarray : None
xlrd : 1.2.0
xlwt : None
xlsxwriter : None
numba : None
```

