-- Lua filter to convert footnotes to endnotes (static text)
-- This collects all footnotes and places them at the end of the document.
-- It also merges consecutive footnotes into a single superscript marker (e.g., 1,2,3).

local List = require 'pandoc.List'
local utils = require 'pandoc.utils'

local notes = List:new()

function Inlines(inlines)
  local new_inlines = List:new()
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if el.t == 'Note' then
      -- Found a note, check for subsequent notes
      local current_indices = {}
      
      -- Process this note
      local num = #notes + 1
      notes[num] = el.content
      table.insert(current_indices, num)
      
      -- Look ahead for more notes
      local j = i + 1
      while j <= #inlines do
        local next_el = inlines[j]
        if next_el.t == 'Note' then
          local next_num = #notes + 1
          notes[next_num] = next_el.content
          table.insert(current_indices, next_num)
          j = j + 1
        elseif next_el.t == 'Space' then
           -- Skip spaces between notes
           j = j + 1
        elseif next_el.t == 'Str' and next_el.text == ',' then
            -- Skip commas between notes (if they exist in source)
            j = j + 1
        else
           break
        end
      end
      
      -- Create the combined marker
      local marker_inlines = List:new()
      for k, idx in ipairs(current_indices) do
        if k > 1 then
          marker_inlines:insert(pandoc.Str(",")) -- Comma separator
        end
        local anchor = "endnote-" .. idx
        marker_inlines:insert(pandoc.Link(pandoc.Str(tostring(idx)), "#" .. anchor))
      end
      
      new_inlines:insert(pandoc.Superscript(marker_inlines))
      
      -- Advance main loop
      i = j
    else
      new_inlines:insert(el)
      i = i + 1
    end
  end
  return new_inlines
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
      
      -- We want: 1. Note content...
      -- note_content is a list of blocks.
      note_list:insert(note_content)
    end
    
    blocks:insert(pandoc.OrderedList(note_list))
  end
  
  return pandoc.Pandoc(blocks, doc.meta)
end
