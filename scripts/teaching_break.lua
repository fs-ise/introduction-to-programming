-- Render semantic teaching breaks with the PDF-specific LaTeX environment.
function Div(div)
  if FORMAT:match("latex") and div.classes:includes("teaching-break") then
    local blocks = { pandoc.RawBlock("latex", "\\begin{teachingbreak}") }
    for _, block in ipairs(div.content) do
      table.insert(blocks, block)
    end
    table.insert(blocks, pandoc.RawBlock("latex", "\\end{teachingbreak}"))
    return blocks
  end
end
