-- Lua filter to convert footnotes to endnotes (static text)
-- This collects all footnotes and places them at the end of the document.

local List = require 'pandoc.List'
local utils = require 'pandoc.utils'

local notes = List:new()

function Note(el)
  -- Get the index for this note
  local num = #notes + 1
  
  -- Store the note content
  notes[num] = el.content
  
  -- Return a superscript number linking to the endnote
  -- We create a link to the endnote anchor
  local anchor = "endnote-" .. num
  local backlink = "ref-" .. num
  
  -- Create the marker in the text: superscript number
  return pandoc.Superscript(pandoc.Link(pandoc.Str(tostring(num)), "#" .. anchor))
end

function Pandoc(doc)
  local blocks = doc.blocks
  
  if #notes > 0 then
    -- Add a separator or heading
    blocks:insert(pandoc.Header(1, "Notes"))
    
    local note_list = List:new()
    
    for i, note_content in ipairs(notes) do
      local anchor = "endnote-" .. i
      local backlink = "ref-" .. i
      
      -- Prepend the number and a backlink to the note content
      -- We want: 1. Note content...
      
      -- Create a list item for the note
      -- We can use an OrderedList for automatic numbering
      -- But to handle the content blocks correctly, let's just use blocks.
      
      -- Actually, putting them in an OrderedList is the cleanest way to format them.
      -- But we need to ensure the blocks inside are handled.
      -- note_content is a list of blocks.
      
      -- Let's try to make it a simple OrderedList
      note_list:insert(note_content)
    end
    
    blocks:insert(pandoc.OrderedList(note_list))
  end
  
  return pandoc.Pandoc(blocks, doc.meta)
end
