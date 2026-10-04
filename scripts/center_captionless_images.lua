-- Center standalone, captionless Markdown images in the teaching-notes PDF.
-- Proper figures (including generated plots) use Quarto's `fig-align` default;
-- this filter covers the image-only paragraphs that Quarto does not promote to
-- figures.

local function has_explicit_alignment(image)
  return image.attributes["fig-align"] ~= nil
    or image.attributes["align"] ~= nil
end

function Para(paragraph)
  if not FORMAT:match("latex") or #paragraph.content ~= 1 then
    return nil
  end

  local image = paragraph.content[1]
  if image.t ~= "Image"
    or #image.caption ~= 0
    or has_explicit_alignment(image) then
    return nil
  end

  return {
    pandoc.RawBlock("latex", "\\begin{center}"),
    paragraph,
    pandoc.RawBlock("latex", "\\end{center}"),
  }
end
