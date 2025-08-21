#!/usr/bin/env python3
import argparse
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="generate_ast",
        description="Generate the Expr.java file for the Lox interpreter AST."
    )
    parser.add_argument(
        "output_dir",
        help="Output directory for the generated file (e.g., path/to/dir)"
    )
    args = parser.parse_args()

    define_ast(args.output_dir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right",
    ])

def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    """Generate the base AST class and its subclasses into a .java file."""
    path = Path(output_dir) / f"{base_name}.java"
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as writer:
        writer.write("package comp.craftinginterpreters.lox;\n\n")
        writer.write("import java.util.List;\n\n")
        writer.write(f"abstract class {base_name} {{\n")

        for type_def in types:
            class_name, fields = [part.strip() for part in type_def.split(":", 1)]
            define_type(writer, base_name, class_name, fields)

        writer.write("}\n")

def define_type(writer, base_name: str, class_name: str, field_list: str) -> None:
    """Write the definition of a subclass of the AST base class."""
    writer.write(f"\tstatic class {class_name} extends {base_name} {{\n")
    writer.write(f"\t\t{class_name}({field_list}) {{\n")

    fields = [f.strip() for f in field_list.split(",")]
    for field in fields:
        name = field.split()[-1]
        writer.write(f"\t\t\tthis.{name} = {name};\n")

    writer.write("\t\t}\n\n")

    for field in fields:
        writer.write(f"\t\tfinal {field};\n")

    writer.write("\t}\n")

if __name__ == "__main__":
    main()

