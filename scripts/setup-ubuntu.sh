#!/usr/bin/env bash

# exit when a command fails instead of blindly blundering forward
set -e
# treat unset variables as an error and exit immediately
set -u
# don't hide exit codes when pipeline output to another command
set -o pipefail

echo "Installing python dependencies"
sudo apt-get update
sudo apt-get -y install --no-install-recommends \
    build-essential \
    curl \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    shellcheck \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev

curl https://pyenv.run | bash

# shellcheck disable=SC2016
{
    echo ''
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
    echo 'eval "$(pyenv init --path)"'
    echo 'eval "$(pyenv init -)"'
    echo 'eval "$(pyenv virtualenv-init -)"'
 } >> ~/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

"$PYENV_ROOT"/bin/pyenv install

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | "$PYENV_ROOT"/shims/python -

echo "Installing all of our python dependencies using Poetry."
"$HOME"/.local/bin/poetry install

echo "Installing pre-commit."
curl https://pre-commit.com/install-local.py | "$PYENV_ROOT"/shims/python -
"$HOME"/bin/pre-commit install

# shellcheck disable=SC2016
{
    echo ''
    echo 'export PATH="$HOME/bin:$PATH"'
} >> ~/.bashrc

curl https://sdk.cloud.google.com > /tmp/install.sh
bash /tmp/install.sh --disable-prompts
rm /tmp/install.sh

# shellcheck disable=SC2016
{
    echo ''
    echo 'export PATH="$HOME/google-cloud-sdk/bin:$PATH"'
} >> ~/.bashrc


echo "Install done."
