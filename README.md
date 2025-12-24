# pa-python-tools
Collection of Python tools and helpers

## Installation

```bash
# Direct installation via repository
pip install git+https://github.com/PierreAnken/pa-python-tools.git

# Or local installation after cloning the project
pip install .
```

### GitHub Configuration

If you are using this package in another project hosted on GitHub, add the following line to your `requirements.txt` file:

```text
pa-python-tools @ git+https://github.com/PierreAnken/pa-python-tools.git
```

## Tools

### json_tools

Provides a custom JSON encoder and decoder to handle types not supported by default by the `json` module.

#### Features

- **Sets**: Automatically converts `set` to a list with a `__set__` marker.
- **Tuples**: Automatically converts `tuple` to a list with a `__tuple__` marker.
- **Datetimes**: Automatically converts `datetime` objects to ISO format with a `__datetime__` marker.
- **Integer keys**: Handles integer keys in dictionaries (which are usually converted to strings by JSON).

#### Usage

```python
import json
from datetime import datetime
from json_tools.json_extension import CustomJSONEncoder, tagged_decoder_hook

data = {
    "my_set": {1, 2, 3},
    "my_tuple": (1, 2, 3),
    "my_date": datetime.now(),
    1: "integer key"
}

# Encoding
json_string = json.dumps(data, cls=CustomJSONEncoder)

# Decoding
decoded_data = json.loads(json_string, object_hook=tagged_decoder_hook)

print(decoded_data)
# Output will have the set, tuple, datetime, and integer key restored correctly.
```

## Development

### Setup

To install development dependencies:

```bash
pip install -e .[dev]
```

### Running Tests

To run the unit tests, ensure you have installed the package in editable mode first (as shown in the [Setup](#setup) section). Then, use one of the following commands:

```bash
# Using unittest
python -m unittest discover tests

# Using pytest (if installed)
pytest
```

Alternatively, if you don't want to install the package, you can set the `PYTHONPATH` manually:

```bash
# Windows (PowerShell)
$env:PYTHONPATH = "src"; python -m unittest discover tests

# Linux / macOS / Git Bash
PYTHONPATH=src python -m unittest discover tests
```
