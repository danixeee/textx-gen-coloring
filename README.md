# Syntax Highlighting Generator for textX Languages

This project uses [textX](https://github.com/textx/textx) grammar and generates syntax highlighting file for it.

Supported syntax highlighting languages:

- textmate (used by VS Code and [textx-gen-vscode](https://github.com/danixeee/textx-gen-vscode) project)

## CLI Examples

Generate a default syntax highlighting for _workflow_ language:

```bash
textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
```

Generate a custom syntax highlighting for _workflow_ language:

```bash
textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow --syntax_spec ./examples/workflow/workflow.txcl
```

## Other Notes

Some parts of code are used from [textX-languageserver](https://github.com/textX/textX-languageserver) project.
