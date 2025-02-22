import json
from pathlib import Path

from base import ErrorList
from python_writer import PythonErrorGenerator

SCRIPT_DIR = Path(__file__).parent


def load_errors() -> ErrorList:
    """Load and parse error definitions from JSON file"""
    json_file = SCRIPT_DIR / "errors.json"
    with open(json_file, "r") as f:
        return ErrorList.model_validate(json.load(f))


def generate_error_codes():
    """Generate error codes from input JSON to output directory"""
    errors = load_errors()
    generators = [PythonErrorGenerator()]

    for generator in generators:
        output_path = Path(generator.get_output_directory())
        code = generator.generate(errors)
        output_file = output_path / generator.get_output_file_name()
        with open(output_file, "w") as f:
            f.write(code)

        print(f"Generated error codes at: {output_file}")


def main():
    generate_error_codes()


if __name__ == "__main__":
    main()
