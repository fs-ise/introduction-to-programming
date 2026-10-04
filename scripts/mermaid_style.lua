-- Apply the shared Mermaid configuration while leaving chart-local init
-- directives in control. Quarto 1.8 bundles Mermaid 11.6, which supports the
-- native handDrawn look used by assets/mermaid-init.json. Its flowchart
-- renderer does not make wrappingWidth or minNodeWidth available reliably, so
-- node sizing is left to Mermaid's normal layout with intentionally compact
-- node padding.

local script = debug.getinfo(1, "S").source:sub(2)
local root = pandoc.path.directory(pandoc.path.directory(script))
local config_path = pandoc.path.join({root, "assets", "mermaid-init.json"})

local config_file = assert(io.open(config_path, "r"))
local config = config_file:read("*a"):gsub("%s+$", "")
config_file:close()

function CodeBlock(block)
  if not block.classes:includes("mermaid") then
    return nil
  end

  if block.text:match("%%%%{%s*[Ii][Nn][Ii][Tt]%s*:") then
    return nil
  end

  block.text = "%%{init: " .. config .. "}%%\n" .. block.text
  return block
end
