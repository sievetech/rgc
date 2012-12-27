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

To use as a library, your python code must call `collect` passing your username, apikey and an instance of the RuleSet class with the rules you want as kwargs:

```python
import rgc.collect
from rgc.rules import RuleSet


rgc.collect('john', '12345abcd', RuleSet(rule1=param1, rule2=param2))
```

You can create your own set of rules by inheriting from RuleSet and defining rule methods. These methods must receive two parameters in addition to `self`:

1. an instance of cloudfiles.Object (see [python-cloudfiles](http://pypi.python.org/pypi/python-cloudfiles));
2. the parameter(s) for the rule, given when the ruleset is instantiated.

```python
import rgc.collect
from rgc.rules import RuleSet


class MyRuleSet(RuleSet):

    def exact_name_rule(self, obj, name):
        return obj.name == name


# will delete all files whose name is 'paper.odt'
rgc.collect('john', '12345abcd', MyRuleSet(exact_name='paper.odt')
```

2) Authors, Copyright and License
---
rgc is Copyright 2012 [Sieve Tecnologia](http://sieve.com.br/).
rgc was written by:
 * [Dalton Matos](https://github.com/daltonmatos)
 * [Elias Tandel Barrionovo](https://github.com/etandel)
 * [Jesué Junior](https://github.com/jesuejunior)

rgc is licensed under 3-BSD. See LICENSE.txt for more details.

