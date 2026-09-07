local function html_escape(value)
  return value:gsub("&", "&amp;")
    :gsub('"', "&quot;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;")
end

local function qrcode(args, kwargs)
  if not quarto.doc.is_format("html") then
    return pandoc.Str("")
  end

  local value = pandoc.utils.stringify(args[1] or "")
  local width = tonumber(pandoc.utils.stringify(kwargs.width or "200")) or 200
  local height = tonumber(pandoc.utils.stringify(kwargs.height or tostring(width))) or width

  quarto.doc.add_html_dependency({
    name = "qrcode",
    version = "1.0.0",
    scripts = { "qrcode.js" }
  })

  return pandoc.RawInline("html", string.format(
    '<div class="qrcode" data-qrcode="%s" data-width="%d" data-height="%d"></div>',
    html_escape(value), width, height
  ))
end

return { qrcode = qrcode }
