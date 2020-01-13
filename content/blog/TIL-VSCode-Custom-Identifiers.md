---
publish:
  - medium
  - blog
written: "2020_01_11"
title: "How to associate a custom extension with a language in VSCode"
lead: "This clever little trick saves me a ton of time when I want language specific features on a custom file extension..."
---

# How to associate a custom extension with a language in VSCode

This clever little trick saves me a ton of time when I want language specific features on a custom file.

In my present example, I am working on a blogging project [code here](https://github.com/NewMountain/Blog). I wanted to use Jinja2 templates and identify them with the `.j2` extension. However, for all other purposes, I wanted VSCode to treat them like HTML files. Most importantly, I am addicted to VSCode's autoformat on save, so I found you can add custom identifiers to VSCode by: `CTRL/CMD + Shift + P` > `Preferences: Open Settings (JSON)` > then adding a little `JSON` in the preferences like so:

```json
/// Place your settings in this file to overwrite the default settings
{
  /// ... Your other settings
  "files.associations": {
    "*.j2": "html"
  }
}
```

and **BOOM!** you can now have custom extensions that still text highlight and behave (auto format) like the underlying file extension type. Lovely!
