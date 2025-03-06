import os
from pathlib import Path

from base import ErrorGenerator, ErrorList


class GoErrorGenerator(ErrorGenerator):
    def generate(self, errorList: ErrorList) -> str:
        code = [
            "// Generated error codes - DO NOT MODIFY MANUALLY",
            "",
            "package generated",
            "",
            "// ErrorCode represents an error code with an associated HTTP status code",
            "type ErrorCode struct {",
            "    Code           string",
            "    HTTPStatusCode int",
            "}",
            "",
            "// Error code constants",
            "var (",
        ]

        for i, error in enumerate(errorList.errors):
            var_name = self._to_go_var_name(error.code)
            code.append(f"    // {error.description}")
            code.append(
                f'    {var_name} = ErrorCode{{Code: "{error.code}", HTTPStatusCode: {error.httpStatusCode}}}'
            )

            if i < len(errorList.errors) - 1:
                code.append("")

        code.append(")")
        code.append("")

        return "\n".join(code)

    def _to_go_var_name(self, code: str) -> str:
        """Convert SNAKE_CASE to GoStyleCamelCase for variable names."""
        parts = code.split("_")
        result = []

        for part in parts:
            result.append(part.lower().capitalize())

        return "".join(result)

    def get_output_directory(self) -> str:
        output_dir = os.getenv(
            "GO_UMA_SDK_OUTPUT_DIR",
            "../uma-go-sdk/uma/generated",
        )
        if not Path(output_dir).exists():
            raise ValueError(
                f"Output directory '{output_dir}' not found. Please ensure the uma-go-sdk repository is checked out "
                "as a sibling directory, or set GO_UMA_SDK_OUTPUT_DIR environment variable to specify an alternate location."
            )
        return output_dir

    def get_output_file_name(self) -> str:
        return "error_codes.go"
