# Contributor's Guide

1. Fork it!

2. Clone the repository

```bash
git clone https://github.com/ktmeaton/NCBImeta.git
cd NCBImeta
```

3. Choose a branch to be your starting point (```master``` or ```dev```).

```bash
git checkout master
```

4. Create a branch for your new feature.

```bash
git checkout -b my-new-feature
```

5. Install dependencies, including developer pre-requisites.

```bash
pip install .[dev]
```

6. Install pre-commit hooks for linting and formatting misc.

```bash
pre-commit install
```

7. Implement your changes/features, add the files, commit the changes.

```bash
git add changed-file.ext
git commit -m "descriptive message of changes"
git push origin
```

8. When ready, submit a pull request (PR) through GitHub. Complete the PR checklist.
