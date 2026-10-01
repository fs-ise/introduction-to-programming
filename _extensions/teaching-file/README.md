# Teaching file extension

The `teaching-file` shortcode displays a Python source file with a download
link and a label for its teaching purpose. For example:

```qmd
{{< teaching-file example.py kind="exercise" >}}
```

In PDF/LaTeX output, long callouts are split across pages by default. The
`max-lines` option controls the approximate number of rendered code lines in
each callout and defaults to `45`:

```qmd
{{< teaching-file example.py max-lines="60" >}}
```

An explicitly supplied positive integer always overrides the default. Use
`split="false"` to disable PDF splitting, or `split="true"` to request it
explicitly. Splitting does not apply to HTML output.

The `kind` option accepts `exercise` (the default), `demo`, `homework`, and
`homework-solution`. Set `callout="false"` to render an unboxed download row
and code block.
