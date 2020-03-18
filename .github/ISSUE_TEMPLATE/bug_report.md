---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ktmeaton

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior (choose all relevant steps):
1. Attach your config.yaml file (remove sensitive data like email and API key!)
2. List the commands that occur before and during the error:
```
NCBImeta.py --flat --config example/config.yaml
NCBImetaAnnotateReplace.py --database example/yersinia_pestis_db.sqlite --annotfile example/annot.txt --table BioSample
```

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**System (please complete the following information):**
 - OS: [e.g. Ubuntu 18.04]
 - Python: [eg. Python 3.7.3]
 - NCBImeta: [eg. NCBImeta v0.6.5]

**Additional context**
Add any other context about the problem here.
