# textx-gen-coloring

A syntax highlight generator for any textX language.

NOTE: Some parts of code are used from [textX-languageserver](https://github.com/textX/textX-languageserver) project.

## CLI examples

Generate a default syntax highlighting for _workflow_ language:

```bash
textX generate --target textmate ./examples/workflow/workflow.tx
```

Generate a custom syntax highlighting for _workflow_ language:

```bash
textX generate --target textmate ./examples/workflow/workflow.tx --cl ./examples/workflow/workflow.txcl
```
