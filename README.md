# traffic-counter

## Setup for Devcontainer/Codespaces

1. Create a Codespace or open in VS Code locally

    Follow Github instructions to [Create a Codespace](https://docs.github.com/en/codespaces/developing-in-codespaces/creating-a-codespace) for this project, or VS Code instructions to [open repo in container](https://code.visualstudio.com/docs/remote/containers-tutorial)

1. Test your installation!

    ```sh
    poetry run traffic-counter --help
    ```

    *or*

    ```sh
    poetry shell
    traffic-counter --help
    ```

## Setup for Mac

1. Install homebrew (if you don't already have it):

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

1. Initialize xcode (if you haven't already):

    ```sh
    xcode-select --install
    ```

1. Install required system deps:

    ```sh
    brew update
    brew install openssl readline sqlite3 xz zlib
    ```

1. Install `pyenv` (if you don't already have it):

    ```sh
    brew update
    brew install pyenv
    ```

    Add `pyenv` to `.zprofile`:

    ```sh
    {
        echo ''
        echo 'eval "$(pyenv init --path)"'
    } >> ~/.zprofile
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.zprofile
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:

    ```sh
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version:

    ```sh
    pyenv install
    ```

    Check correct `python`  version was installed by verifying it matchings `.python-version`:

    ```sh
    python --version
    cat .python-version
    ```

1. Install `poetry` into the current python version:

    ```sh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
    ```

1. Add `poetry` to `.bashrc` (or `.zshrc` if you use `zsh`):

    ```sh
    {
        echo ''
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.bashrc
    ```

1. Install app into local poetry managed `.venv`:

    ```sh
    poetry install
    ```

1. Test your installation!

    ```sh
    poetry run traffic-counter --help
    ```

    *or*

    ```sh
    poetry shell
    traffic-counter --help
    ```

1. Install `pre-commit`:

    ```sh
    brew install pre-commit
    pre-commit install
    ```

1. Install gcloud SDK:

    ```sh
    brew install --cask google-cloud-sdk
    gcloud init
    ```

## Setup for Ubuntu/Debian

1. Install required system deps:

    ```sh
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

    ```sh
    curl https://pyenv.run | bash
    ```

    Add `pyenv` to `.bashrc` (or `.zshrc` if you use `zsh`):

    ```sh
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

    ```sh
    source ~/.bashrc
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:

    ```sh
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version:

    ```sh
    pyenv install
    ```

    Check correct `python`  version was installed by verifying it matchings `.python-version`:

    ```sh
    python --version
    cat .python-version
    ```

1. Install `poetry` into the current python version:

    ```sh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
    ```

1. Add `poetry` to `.bashrc` (or `.zshrc` if you use `zsh`):

    ```sh
    {
        echo ''
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.bashrc
    ```

1. Install app into local poetry managed `.venv`:

    ```sh
    poetry install
    ```

1. Test your installation!

    ```sh
    poetry run traffic-counter --help
    ```

    *or*

    ```sh
    poetry shell
    traffic-counter --help
    ```

1. Install `pre-commit`:

    ```sh
    curl https://pre-commit.com/install-local.py | python -
    pre-commit install
    ```

1. Install gcloud SDK:

    ```sh
    curl https://sdk.cloud.google.com | bash
    gcloud init
    ```

## Usage

1. Run tests

    ```sh
    poetry run tox
    ```

    Just tests:

    ```sh
    poetry run tox -qe test
    ```

    Just lint:

    ```sh
    poetry run tox -qe lint
    ```

1. Start server

    ```sh
    poetry run traffic-counter serve
    ```
