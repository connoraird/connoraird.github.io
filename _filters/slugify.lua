-- Slugify titles for use in URLs or identifiers.
local function slugify(s)
    -- Convert spaces/slashes to hyphens
    s = s:gsub("[%s+/]+", "-")
    -- Remove non-alphanumeric/non-hyphen characters and convert to lowercase
    return s:gsub("[^%w-]+", ""):lower()
end

local function combine_and_slugify(...)
    local rawparts = {...}
    local parts = {}
    for i, part in pairs(rawparts) do
        parts[i] = pandoc.utils.stringify(part)
    end
    local combined = table.concat(parts, " ")
    return slugify(combined)
end

return {
    Meta = function(m)
        -- Example: combine date, title, and author
        m.slug = combine_and_slugify(m.date, m.title)
        return m
    end,
}
