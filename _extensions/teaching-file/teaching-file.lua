local kinds = {
  exercise = { label = "In-class exercise" },
  demo = { label = "In-class demo" },
  homework = { label = "Homework" },
  ["homework-solution"] = { label = "Homework solution", style = "homework" },
}

local function teaching_file(args, kwargs)
  kwargs = kwargs or {}
  local path = pandoc.utils.stringify(args[1] or "")
  if path == "" then
    error("teaching-file shortcode requires a filepath as its first argument")
  end

  local kind = pandoc.utils.stringify(kwargs["kind"])
  if kind == "" then
    kind = "exercise"
  end
  local kind_config = kinds[kind]
  if kind_config == nil then
    error("teaching-file shortcode: unknown kind '" .. kind ..
      "' (expected exercise, demo, homework, or homework-solution)")
  end
  local style = kind_config.style or kind

  local input_dir = pandoc.path.directory(quarto.doc.input_file or "")
  local source_path = pandoc.path.join({ input_dir, path })
  local source = io.open(source_path, "r")
  if not source then
    error("teaching-file shortcode: source file does not exist: " .. path)
  end
  local contents = source:read("*a")
  source:close()

  local label = pandoc.Span(
    kind_config.label,
    pandoc.Attr("", { "teaching-label", "teaching-label-" .. style })
  )
  local link = pandoc.Link(
    { pandoc.Code(pandoc.path.filename(path)) },
    path,
    "",
    pandoc.Attr("", { "teaching-button", "teaching-button-" .. style })
  )
  local download = pandoc.Div(
    { pandoc.Para({ label, pandoc.Space(), link }) },
    pandoc.Attr("", { "teaching-file" })
  )
  local code = pandoc.CodeBlock(
    contents,
    pandoc.Attr("", { "python" }, { eval = "false" })
  )

  return pandoc.Blocks({ download, code })
end

return { ["teaching-file"] = teaching_file }
