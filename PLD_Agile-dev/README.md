# PDL Agile

## Installation

1. Install Python 3.10 (skip this step if you already have Python 3.10 installed)

    1. Install [pyenv](https://github.com/pyenv/pyenv)

    2. Install Python version

    ```bash
    pyenv install 3.10
    ```

    3. Switch to Python version

    ```bash
    pyenv shell 3.10
    ```

2. Install [pipenv](https://pipenv.pypa.io/en/latest/)

```bash
pip install --user pipenv
```

3. Create virtual environment directory

```bash
mkdir .venv
```

4. Create virtual environment and install dependencies

```bash
python -m pipenv install --dev --python 3.10
```

5. Activate virtual environment

```bash
pipenv shell
```

or

```bash
source .venv/bin/activate
```

6. Check if everything is working

```bash
python --version
```

## Execution

1. Go to tab `Run and Debug` in VSCode (shortcut: `Ctrl + Shift + D`)

2. Select `Python: Main` in dropdown

3. Press `F5` to run the program or click `Run` button

## Tests

1. Go to tab `Testing` in VSCode (shortcut: `Ctrl + Shift + T`)

2. Click `Run Tests` button

## Format code

```bash
# Format code
black src/
# Sort imports
isort src/
```