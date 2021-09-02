# traffic-counter

## Setup for Codespaces

1. Create a Codespace

    Follow Github instructions to [Create a Codespace](https://docs.github.com/en/codespaces/developing-in-codespaces/creating-a-codespace) for this project.

1. Test your installation!

    ```
    poetry run traffic-counter --help
    ```

    *or*

    ```
    poetry shell
    traffic-counter --help
    ```

## Setup for Mac

1. Install homebrew (if you don't already have it):

    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

1. Initialize xcode (if you haven't already):

    ```
    xcode-select --install
    ```

1. Install required system deps:

    ```
    brew update
    brew install openssl readline sqlite3 xz zlib
    ```

1. Install `pyenv` (if you don't already have it):

    ```
    brew update
    brew install pyenv
    ```

    Add `pyenv` to `.zprofile`:
    ```
    {
        echo ''
        echo 'eval "$(pyenv init --path)"'
    } >> ~/.zprofile
    ```

    Refresh current shell with updated paths:
    ```
    source ~/.zprofile
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:
    ```
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version:

    ```
    pyenv install
    ```

1. Install `poetry` into the current python version:

    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
    ```

1. Add `poetry` to `.bashrc` (or `.zshrc` if you use `zsh`):

    ```
    {
        echo ''
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:
    ```
    source ~/.bashrc
    ```

    Check correct `python`  version was installed by verifying it matchings `.python-version`:
    ```
    python --version
    cat .python-version
    ```

1. Install app into local poetry managed `.venv`:

    ```
    poetry install
    ```

1. Test your installation!

    ```
    poetry run traffic-counter --help
    ```

    *or*

    ```
    poetry shell
    traffic-counter --help
    ```

## Setup for Ubuntu/Debian

1. Install required system deps:

    ```
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
    ```

1. Install `pyenv` (if you don't already have it):

    ```
    curl https://pyenv.run | bash
    ```

    Add `pyenv` to `.bashrc` (or `.zshrc` if you use `zsh`):
    ```
    {
        echo ''
        echo 'export PYENV_ROOT="$HOME/.pyenv"'
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
        echo 'eval "$(pyenv init --path)"'
        echo 'eval "$(pyenv init -)"'
        echo 'eval "$(pyenv virtualenv-init -)"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:
    ```
    source ~/.bashrc
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:
    ```
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version:

    ```
    pyenv install
    ```

1. Install `poetry` into the current python version:

    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
    ```

1. Add `poetry` to `.bashrc` (or `.zshrc` if you use `zsh`):

    ```
    {
        echo ''
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:
    ```
    source ~/.bashrc
    ```

    Check correct `python`  version was installed by verifying it matchings `.python-version`:
    ```
    python --version
    cat .python-version
    ```

1. Install app into local poetry managed `.venv`:

    ```
    poetry install
    ```

1. Test your installation!

    ```
    poetry run traffic-counter --help
    ```

    *or*

    ```
    poetry shell
    traffic-counter --help
    ```

## Usage

1. Start server

    ```
    poetry run traffic-counter serve
    ```
