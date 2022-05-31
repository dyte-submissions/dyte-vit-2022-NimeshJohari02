# clone a single file from a git repository
# Usage: cloneSingleFile.bash <repository> <file> <destination>
# Example: cloneSingleFile.bash

git clone $1
cd $2
git checkout $3
