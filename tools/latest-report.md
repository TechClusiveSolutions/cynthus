```
suite                                          passed failed xfail skip  stmts  miss   cover
--------------------------------------------------------------------------------------------
cynthus-core/api                                   46      0     1    0    128     2   98.4%
cynthus-core/inventory                             42      0     1    0    128     2   98.4%
cynthus-core/logistics                             69      0     1    0    186     2   98.9%
cynthus-core/profile                               46      0     1    0    128     2   98.4%
cynthus-core/recipe                                46      0     1    0    128     2   98.4%
cynthus-core/scheduler                             19      0     0    0     38     0  100.0%
cynthus-core/shopping                              46      0     1    0    128     2   98.4%
cynthus-core/web                                   27      0     0    0     47     0  100.0%
cynthus-core/worker                                14      0     0    0     19     0  100.0%
cynthus-health/api                                 27      0     0    0     47     0  100.0%
cynthus-health/web                                 27      0     0    0     47     0  100.0%
cynthus-intelligence/analysis                      29      0     1    0     57     0  100.0%
cynthus-intelligence/chat                          27      0     0    0     47     0  100.0%
cynthus-messaging                                 138      0     0    2     29     0  100.0%
cynthus-messaging-core                           1348      0     1    0    761     8   98.9%
cynthus-mocks/analysis                             16      0     0    0     17     0  100.0%
cynthus-mocks/auth                                 16      0     0    0     17     0  100.0%
cynthus-mocks/chat                                 16      0     0    0     17     0  100.0%
cynthus-mocks/portal-api                           16      0     0    0     17     0  100.0%
cynthus-mocks/portal-web                           16      0     0    0     17     0  100.0%
cynthus-trust/auth                                 27      0     0    0     47     0  100.0%
--------------------------------------------------------------------------------------------
TOTAL (parsable source)                          2058      0     8    2   2050    20   99.0%
TOTAL incl. unparsable files as 0 %                                       2050    20   99.0%

Parsable files coverage.py did not report on - 2 files:
  cynthus-messaging\src\cynthus\messaging\__init__.py
  cynthus-messaging\src\cynthus\messaging\component\__init__.py

Threshold 75 %: parsable source MEETS, including unparsable MEETS

cynthus-web (node): 64 passed, 0 failed; line coverage 93.37 %, branch 78.41 %, functions 85.14 %
```
