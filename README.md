rgc
===
Rackspace Garbage Collector:

A library and a tool for removing Rackspace Files in an more efficient manner.

1) About
---
Rackspace Garbage Collector is a python library and a tool that helps the user to remove unused / useless files stored in Rackspace.

To use as a command line program, just run
```shell
user=johndoe key=12345abcd rgc --rule1 param1 --rule2 param2
```
where the rules are checks applied to each file to determine if it should be deleted or not. For example, `--days 30` will remove all files older than 30 days. If more than one rule is given, they are AND'd together, i.e. a file will be removed if, and only if, it meets all conditions.

To use as a library, your python code must call `collect` passing your username, apikey and a rule:

```python
import rgc.collect
from rgc.rules import olderthan


rgc.collect('john', '12345abcd', olderthan(30))
```

You can create your own rules by decorating functions with the `rule` decorator. These functions should receive the cloudfile object as first argument along with other relevant parameters.

```python
import rgc.collect
from rgc.rules import rule


@rule
def public(obj, ispublic):
    return obj.container.is_public() == is_public


# will delete all files whose container is public (if that's useful somehow...)
rgc.collect('john', '12345abcd', public(True))
```

Rules can be combined using & (and), | (or) and ~ (not).

```
import rgc.collect
from rgc.rules import olderthan, namehassuffix, namehasprefix

is_useless_xls = olderthan(30) #older than 30 days
is_useless_xls &= namehassuffix('.xls')  #is a spreadsheet file
is_useless_xls &= (~namehasprefix('IMPORTANT')) #but is not important

# will delete all 'useless' xls files:
rgc.collect('john', '12345abcd', is_useless_xls)
```

2) Authors, Copyright and License
---
rgc is Copyright 2012 [Sieve Tecnologia](http://sieve.com.br/).
rgc was written by:
 * [Dalton Matos](https://github.com/daltonmatos)
 * [Elias Tandel Barrionovo](https://github.com/etandel)
 * [Jesué Junior](https://github.com/jesuejunior)

rgc is licensed under 3-BSD. See LICENSE.txt for more details.

