install:
# Install Anaconda
- if [[ $TRAVIS_PYTHON_VERSION == 3.5 && $TRAVIS_TAG == v* ]]; then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
    bash miniconda.sh -b -p $HOME/miniconda
    export PATH="$PATH:$HOME/miniconda/bin"
    hash -r
    conda config --set always_yes yes --set changeps1 no
    conda update -q conda
  fi

after_success:
- if [[ $TRAVIS_PYTHON_VERSION == 3.5 && $TRAVIS_TAG == v* ]]; then
  # Install the utility package to perform an autobump update
  conda install --c bioconda bioconda-utils;

  # Currently in the main program directory, collect basic program info
  program_ver=`NCBImeta.py --version | cut -d " " -f2 | sed 's/v//g'`;

  # Navigate outside the main program repository, download bioconda-recipes
  cd ../ ;
  git clone https://github.com/${GITHUB_USER}/bioconda-recipes.git;
  cd bioconda-recipes/;

  # Switch to the master branch
  git checkout master;

  # Setup some basic parameters
  git config user.name $GITHUB_USER;
  git config user.email $GITHUB_USER_EMAIL;

  # Retrieve updates that might be missing in local repo
  git remote add upstream https://github.com/bioconda/bioconda-recipes.git;
  git pull upstream master;

  bioconda-utils autobump recipes/ config.yml --packages ${program_name}
fi
