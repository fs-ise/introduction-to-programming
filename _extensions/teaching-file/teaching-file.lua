local DEFAULT_MAX_LINES = 38
local APPROX_CODE_COLUMNS = 72
local CALLOUT_OVERHEAD_LINES = 5

local kinds = {
  exercise = { label = "In-class exercise" },
  demo = { label = "In-class demo" },
  homework = { label = "Homework" },
  ["homework-solution"] = { label = "Homework solution", style = "homework" },
}

local function option_text(value)
  return pandoc.utils.stringify(value)
end

local function parse_boolean(value, name, default)
  local text = option_text(value)
  if text == "" then
    return default
  end

  text = string.lower(text)
  if text == "true" then
    return true
  elseif text == "false" then
    return false
  end

  error("teaching-file shortcode: " .. name .. " must be 'true' or 'false' (got '" ..
    text .. "')")
end

local function parse_split(value)
  local text = string.lower(option_text(value))
  if text == "" then
    return "auto"
  end
  if text == "auto" or text == "true" or text == "false" then
    return text
  end

  error("teaching-file shortcode: split must be 'auto', 'true', or 'false' (got '" ..
    text .. "')")
end

local function parse_positive_integer(value, name, default)
  local text = option_text(value)
  if text == "" then
    return default
  end
  if not string.match(text, "^%d+$") or tonumber(text) <= 0 then
    error("teaching-file shortcode: " .. name ..
      " must be a positive integer (got '" .. text .. "')")
  end
  return tonumber(text)
end

local function is_latex_output()
  if quarto.doc.is_format then
    return quarto.doc.is_format("latex") or quarto.doc.is_format("pdf")
  end

  -- FORMAT is supplied by Pandoc. The fallback also makes the extension easy
  -- to exercise outside Quarto's normal render pipeline.
  local format = string.lower(FORMAT or "")
  return string.find(format, "latex", 1, true) ~= nil or
    string.find(format, "beamer", 1, true) ~= nil
end

local function source_lines(contents)
  local lines = {}
  local start = 1
  while true do
    local newline = string.find(contents, "\n", start, true)
    if not newline then
      if start <= #contents then
        table.insert(lines, string.sub(contents, start))
      end
      break
    end
    table.insert(lines, string.sub(contents, start, newline - 1))
    start = newline + 1
  end
  return lines
end

local function rendered_lines(line)
  local length = utf8.len(line) or #line
  return math.max(1, math.ceil(length / APPROX_CODE_COLUMNS))
end

local function rendered_line_count(contents)
  local count = 0
  for _, line in ipairs(source_lines(contents)) do
    count = count + rendered_lines(line)
  end
  return count
end

local function split_source(contents, max_lines)
  local lines = source_lines(contents)
  local chunks = {}
  local first = 1

  while first <= #lines do
    local last = first - 1
    local effective_lines = 0
    local preferred_blank = nil

    while last < #lines do
      local candidate = last + 1
      local candidate_lines = rendered_lines(lines[candidate])
      if last >= first and effective_lines + candidate_lines > max_lines then
        break
      end
      last = candidate
      effective_lines = effective_lines + candidate_lines
      if effective_lines >= math.ceil(max_lines / 2) and
          string.match(lines[last], "^%s*$") then
        preferred_blank = last
      end
    end

    -- Prefer a blank line in the latter half of the prospective chunk. This
    -- keeps related code together without creating tiny continuation pages.
    if last < #lines and preferred_blank then
      last = preferred_blank
    end

    local chunk_lines = {}
    for index = first, last do
      table.insert(chunk_lines, lines[index])
    end
    table.insert(chunks, table.concat(chunk_lines, "\n"))
    first = last + 1
  end

  return chunks
end

local function make_label(kind_config, style)
  return pandoc.Span(
    kind_config.label,
    pandoc.Attr("", { "teaching-label", "teaching-label-" .. style })
  )
end

local function make_link(path, style)
  return pandoc.Link(
    { pandoc.Code(pandoc.path.filename(path)) },
    path,
    "",
    pandoc.Attr("", { "teaching-button", "teaching-button-" .. style })
  )
end

local function make_title(path, kind_config, style, continued)
  local title = pandoc.Inlines({
    make_label(kind_config, style),
    pandoc.Space(),
    make_link(path, style),
  })
  if continued then
    title:extend({
      pandoc.Space(), pandoc.Str("—"), pandoc.Space(),
      pandoc.Str("continued"), pandoc.Space(), pandoc.Str("from"),
      pandoc.Space(), pandoc.Str("previous"), pandoc.Space(), pandoc.Str("page"),
    })
  end
  return title
end

local function make_code(contents)
  return pandoc.CodeBlock(
    contents,
    pandoc.Attr("", { "python" }, { eval = "false" })
  )
end

local function make_callout(path, contents, kind_config, style, continued)
  return quarto.Callout({
    type = "tip",
    title = make_title(path, kind_config, style, continued),
    content = { make_code(contents) },
  })
end

local function teaching_file(args, kwargs)
  kwargs = kwargs or {}
  local path = option_text(args[1] or "")
  if path == "" then
    error("teaching-file shortcode requires a filepath as its first argument")
  end

  local kind = option_text(kwargs["kind"])
  if kind == "" then
    kind = "exercise"
  end
  local kind_config = kinds[kind]
  if kind_config == nil then
    error("teaching-file shortcode: unknown kind '" .. kind ..
      "' (expected exercise, demo, homework, or homework-solution)")
  end
  local style = kind_config.style or kind
  local use_callout = parse_boolean(kwargs["callout"], "callout", true)
  local split = parse_split(kwargs["split"])
  local max_lines = parse_positive_integer(kwargs["max-lines"], "max-lines", DEFAULT_MAX_LINES)

  local input_dir = pandoc.path.directory(quarto.doc.input_file or "")
  local source_path = pandoc.path.join({ input_dir, path })
  local source = io.open(source_path, "r")
  if not source then
    error("teaching-file shortcode: source file does not exist: " .. path)
  end
  local contents = source:read("*a")
  source:close()

  if not use_callout then
    local download = pandoc.Div(
      { pandoc.Para({ make_label(kind_config, style), pandoc.Space(), make_link(path, style) }) },
      pandoc.Attr("", { "teaching-file" })
    )
    return pandoc.Blocks({ download, make_code(contents) })
  end

  local chunks = split_source(contents, max_lines)
  local should_split = is_latex_output() and split ~= "false" and #chunks > 1
  if not should_split then
    return make_callout(path, contents, kind_config, style, false)
  end

  local first_chunk_lines = rendered_line_count(chunks[1])
  local result = {
    pandoc.RawBlock("latex", string.format(
      "\\Needspace{%d\\baselineskip}", first_chunk_lines + CALLOUT_OVERHEAD_LINES
    )),
  }
  for index, chunk in ipairs(chunks) do
    if index > 1 then
      result[#result + 1] = pandoc.RawBlock("latex", "\\newpage{}")
    end
    result[#result + 1] = make_callout(path, chunk, kind_config, style, index > 1)
  end
  return pandoc.Blocks(result)
end

return { ["teaching-file"] = teaching_file }
