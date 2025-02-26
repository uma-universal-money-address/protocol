import os
from pathlib import Path

from base import ErrorGenerator, ErrorList


class JsErrorGenerator(ErrorGenerator):
    def generate(self, errorList: ErrorList) -> str:
        code = [
            "/**",
            " * Generated error codes - DO NOT MODIFY MANUALLY",
            " */",
            "",
            "export interface ErrorDetails {",
            "  code: string;",
            "  httpStatusCode: number;",
            "}",
            "",
            "export const ErrorCode = {",
        ]

        for error in errorList.errors:
            code.append(f"  /** {error.description} */")
            code.append(f"  {error.code}: {{")
            code.append(f'    code: "{error.code}",')
            code.append(f"    httpStatusCode: {error.httpStatusCode}")
            code.append("  },")
            code.append("")

        code.append("} as const;")

        return "\n".join(code)

    def get_output_directory(self) -> str:
        output_dir = os.getenv(
            "JS_UMA_SDK_OUTPUT_DIR", "../uma-js-sdk/packages/core/src/generated"
        )
        if not Path(output_dir).exists():
            raise ValueError(
                f"Output directory '{output_dir}' not found. Please ensure the uma-js-sdk repository is checked out "
                "as a sibling directory, or set JS_UMA_SDK_OUTPUT_DIR environment variable to specify an alternate location."
            )
        return output_dir

    def get_output_file_name(self) -> str:
        return "errorCodes.ts"
