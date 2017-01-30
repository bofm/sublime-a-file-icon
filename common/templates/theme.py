TEMPLATE = """[
  // %(name)s Patch
  // ==========================================================================

  // Sidebar File Icons
  // --------------------------------------------------------------------------

  // Default

  {
    "class": "icon_file_type"%(color)s%(opacity)s%(size)s
  },

  // Hovered

  {
    "class": "icon_file_type"%(color_on_hover)s
    "parents": [{"class": "tree_row", "attributes": ["hover"]}]%(opacity_on_hover)s
  },

  // Selected

  {
    "class": "icon_file_type"%(color_on_select)s
    "parents": [{"class": "tree_row", "attributes": ["selected"]}]%(opacity_on_select)s
  }
]
"""
