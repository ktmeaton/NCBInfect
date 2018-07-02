import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NCBImeta",
    version="0.3.1",
    author="Katherine Eaton",
    author_email="ktmeaton@gmail.com",
    description="Creates a SQLite database of metadata from the NCBI database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ktmeaton/NCBImeta",
    packages=setuptools.find_packages(),
    python_requires='>=2.7, <4',
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
