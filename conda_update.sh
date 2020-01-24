#!/bin/bash

# This is a script to update and upload bioconda recipes for pull requests

# Currently in the main program directory, collect basic program info
program_ver=`NCBImeta.py --version | cut -d " " -f2 | sed 's/v//g'`;
program_url=https://github.com/${TRAVIS_REPO_SLUG}/archive/v${program_ver}.tar.gz;
program_name=ncbimeta;
bioconda_recipe=meta.yaml;

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

# Remove the default origin, add in new origin that contains personal access token
git remote rm origin;
git remote add origin https://${GITHUB_USER}:${GITHUB_API_KEY}@github.com/${GITHUB_USER}/bioconda-recipes.git > /dev/null 2>&1;

# Push the new remote updates to the local repo
git push -f -q https://${GITHUB_USER}:${GITHUB_API_KEY}@github.com/${GITHUB_USER}/bioconda-recipes master;
cd recipes/;

# Store the 2 variables to be changed: version and the sha256 hash
dest_ver=`echo "{% set version = \"${program_ver}"\" %}`;
src_ver=`grep "set version" ${program_name}/${bioconda_recipe}`;
dest_sha256=`wget -O- ${program_url} | shasum -a 256 | cut -d " " -f 1`;
src_sha256=`grep "sha256" ${program_name}/${bioconda_recipe} | sed 's/^ *//g' | cut -d " " -f 2`;

# Create a new branch and switch to it for the updated recipe
git checkout -b ${program_name}-${program_ver};

# For debugging, print the first lines of the old recipe
head ${program_name}/${bioconda_recipe};

# Replace the old version and the old sha256 hash
sed -i "s/$src_ver/$dest_ver/g" ${program_name}/${bioconda_recipe};
sed -i "s/$src_sha256/$dest_sha256/g" ${program_name}/${bioconda_recipe};

# For debugging, print the first lines of the new recipe
head ${program_name}/${bioconda_recipe};

# Add, commit, push the new recipe to the new branch
git add ${program_name};
git commit -m "${program_name} v${program_ver} recipe update";
git push --set-upstream origin ${program_name}-${program_ver};

# Return to the original directory
cd ../../NCBImeta/;
