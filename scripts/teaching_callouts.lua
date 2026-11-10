-- Add the locally vendored Lucide vector icons to the native callout titles in PDFs.
local callout_icons = {
  ["teaching-tip"] = "lightbulb",
  ["ask-students"] = "message-circle-question",
  ["common-misconception"] = "triangle-alert",
  ["timing-transition"] = "clock",
  ["instructor-hint"] = "settings",
}

function Callout(callout)
  if not FORMAT:match("latex") or callout.title == nil then
    return
  end

  for class, icon in pairs(callout_icons) do
    if callout.attr.classes:includes(class) then
      local title = quarto.utils.as_inlines(callout.title)
      local icon_image = pandoc.Image(
        {},
        "../assets/icons/" .. icon .. ".pdf",
        "",
        pandoc.Attr("", { "callout-title-icon" }, { width = "0.78em", height = "0.78em" })
      )
      title:insert(1, icon_image)
      title:insert(2, pandoc.RawInline("latex", "\\hspace{0.45em}"))
      callout.title = title
      callout.icon = false
      if class == "instructor-hint" then
        callout.type = "none"
      end
      return callout
    end
  end
end
