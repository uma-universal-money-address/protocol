import os
from pathlib import Path

from base import ErrorGenerator, ErrorList


class KotlinErrorGenerator(ErrorGenerator):
    def generate(self, errorList: ErrorList) -> str:
        code = [
            "/**",
            " * Generated error codes - DO NOT MODIFY MANUALLY",
            " */",
            "",
            "package me.uma.generated",
            "",
            "/**",
            " * Error codes used throughout the UMA SDK",
            " */",
            "enum class ErrorCode(val httpStatusCode: Int) {",
        ]

        for error in errorList.errors:
            code.append(f"    /**")
            code.append(f"     * {error.description}")
            code.append(f"     */")
            code.append(f"    {error.code}({error.httpStatusCode}),")
            code.append("")

        if errorList.errors:
            code.pop()

        code.append("}")
        code.append("")

        return "\n".join(code)

    def get_output_directory(self) -> str:
        output_dir = os.getenv(
            "KOTLIN_UMA_SDK_OUTPUT_DIR",
            "../uma-kotlin-sdk/uma-sdk/src/commonMain/kotlin/me/uma/generated",
        )
        if not Path(output_dir).exists():
            raise ValueError(
                f"Output directory '{output_dir}' not found. Please ensure the uma-kotlin-sdk repository is checked out "
                "as a sibling directory, or set KOTLIN_UMA_SDK_OUTPUT_DIR environment variable to specify an alternate location."
            )
        return output_dir

    def get_output_file_name(self) -> str:
        return "ErrorCode.kt"
