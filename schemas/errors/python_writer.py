import os
from pathlib import Path

from base import ErrorGenerator, ErrorList


class PythonErrorGenerator(ErrorGenerator):
    def generate(self, errorList: ErrorList) -> str:
        code = [
            "from enum import Enum",
            "from dataclasses import dataclass",
            "",
            "@dataclass",
            "class ErrorDetails:",
            "    code: str",
            "    http_status_code: int",
            "",
            "class ErrorCode(Enum):",
        ]

        for error in errorList.errors:
            code.append(
                f'    {error.code} = ErrorDetails(code="{error.code}", http_status_code={error.httpStatusCode})'
            )
            code.append(f'    """{error.description}"""')
            code.append("")

        return "\n".join(code)

    def get_output_directory(self) -> str:
        output_dir = os.getenv(
            "PYTHON_UMA_SDK_OUTPUT_DIR", "../uma-python-sdk/uma/generated"
        )
        if not Path(output_dir).exists():
            raise ValueError(
                f"Output directory '{output_dir}' not found. Please ensure the uma-python-sdk repository is checked out "
                "as a sibling directory, or set PYTHON_UMA_SDK_OUTPUT_DIR environment variable to specify an alternate location."
            )
        return output_dir

    def get_output_file_name(self) -> str:
        return "errors.py"
