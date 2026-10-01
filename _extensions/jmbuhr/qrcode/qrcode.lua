local function html_escape(value)
  return value:gsub("&", "&amp;")
    :gsub('"', "&quot;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;")
end

local function qrcode(args, kwargs)
  local value = pandoc.utils.stringify(args[1] or "")
  local width = tonumber(pandoc.utils.stringify(kwargs.width or "200")) or 200
  local height = tonumber(pandoc.utils.stringify(kwargs.height or tostring(width))) or width

  if quarto.doc.is_format("html") then
    quarto.doc.add_html_dependency({
      name = "qrcode",
      version = "1.0.0",
      scripts = { "qrcode.js" }
    })

    return pandoc.RawInline("html", string.format(
      '<div class="qrcode" style="margin: 12px 0" data-qrcode="%s" data-width="%d" data-height="%d"></div>',
      html_escape(value), width, height
    ))
  end

  if quarto.doc.is_format("latex") then
    -- Center the code vertically and add 2 mm of whitespace above and below.
    local size_cm = math.max(width, height) * 0.015
    local padded_size_cm = size_cm + 0.4
    return pandoc.RawInline("latex", string.format(
      "{\\NoHyper\\rule[-%.2fcm]{0pt}{%.2fcm}\\raisebox{-0.5\\height}{\\color{black}\\qrcode[height=%.2fcm]{%s}}\\endNoHyper}",
      padded_size_cm / 2, padded_size_cm, size_cm, value
    ))
  end

  -- Other formats still receive the destination rather than a blank cell.
  return pandoc.Str(value)
end

return { qrcode = qrcode }
