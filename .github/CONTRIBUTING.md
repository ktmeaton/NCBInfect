# Contributor's Guide

1. **Check for similar [Pull Requests](https://github.com/ktmeaton/NCBImeta/pulls) proposing the same changes/features.**

1. **Fork it!**

1. **Clone your forked repository.**

    ```bash
    git clone https://github.com/myusername/NCBImeta.git
    cd NCBImeta
    ```

1. **Choose an existing branch to be your starting point (ex. ```dev```).**

    ```bash
    git checkout dev
    ```

1. **Create a branch for your new feature.**

    ```bash
    git checkout -b my-new-feature
    ```

1. **Install dependencies, including developer prerequisites.**

    ```bash
    pip install .[dev]
    ```

1. **Install pre-commit hooks for linting and miscellaneous formatting. Check to make sure all files lint before beginning your contribution.**
\*Note: This project formats python files with ```black``` and ```flake8```.

    ```bash
    pre-commit install
    pre-commit run
    pre-commit run --all-files
    ```

1. **Implement your changes/features.**

1. **Update the relevant documentation, ex. the [Config](https://github.com/ktmeaton/NCBImeta/blob/master/config/README_config.md) and [Schema](https://github.com/ktmeaton/NCBImeta/blob/master/schema/README_schema.md) docs.**

1. **Run the test suite, and add new tests if relevant.**

    ```bash
    python \
      -m coverage run \
      -m pytest \
      --cov=ncbimeta \
      --cov-report=html \
      test/test_errors.py \
      test/test_utilities.py \
      test/test_ncbimeta.py \
      test/test_annotateconcatenate.py \
      test/test_annotatereplace.py \
      test/test_join.py \
      test/test_export.py
    ```

1. **Add the changed files to your local repository and commit them.**

    ```bash
    git add changed-file.ext
    git commit -m "descriptive message of changes"
    ```

    This should automatically run all relevant linters. If not, run:

    ```bash
    pre-commit run --all-files
    ```

    If files fail to lint, apply the suggested corrections, and repeat Step 11.

1. **Push the changes to your own github repository.**

    ```bash
    git push origin
    ```

1. **Submit a pull request (PR) on the [original repository](https://github.com/ktmeaton/NCBImeta.git) GitHub. Complete the PR checklist.**
