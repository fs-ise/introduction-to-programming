local function needspace(args)
  if not quarto.doc.is_format("pdf") then
    return pandoc.Str("")
  end

  local lines = pandoc.utils.stringify(args[1] or "5")
  return pandoc.RawInline(
    "latex",
    string.format("\\Needspace{%s\\baselineskip}", lines)
  )
end

return { needspace = needspace }
