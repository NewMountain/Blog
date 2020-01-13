---
publish:
  - medium
  - blog
written: "2020_01_11"
title: "Making a custom blog Pt. 1"
lead: "After a few days of surveying the static content space, I didn't see anything I really liked, so I decided to make my own instead..."
---

# Making a custom blog Pt. 1

After a few days of surveying the static content space, I didn't see anything I really liked, so I decided to make my own instead.
The major points of differentiation for me were:

1. To learn and exercise my brain a bit by doing something myself
2. Blog about stuff as Github flavored Markdown
3. Easily turn that into a blog to that will be hosted in S3
4. Easily cross post any articles I want into other channels (Medium and perhaps others)
5. Automate everything that isn't me writing Markdown or checking code into Github as a CD pipeline

That all seems reasonable so let's dive right in.

## Analysis paralysis

Almost immediately, I felt a little overwhelmed. There were so many choices to make, so many ways to do things and so many lovely open source projects that did 60% of what I wanted while adding a decent bit of complexity and giving me a lot of features I didn't need. I took a deep breath and defined the goals outlined above.

With that, a few things became clear, I wanted to write basically Markdown files, embed the content in an HTML template, upload to [my blog](https://christophernyber.com) and for those markdown I thought would be interesting to cross post, upload the Markdowns to other social media platforms.

The goal was to keep this super modular, so that over time, it would be relatively easy to repost content on Medium as well as alert in places like Twitter and LinkedIn that new content was published.

_One other thing_, I really wanted to do this using a modern functional approach as possible. I have a great deal of thoughts on OOP, but I'll save those for another time... ;).

## How it should work

So my idea is basically, create a `/content` directory. In that directory, you will find an `./assets/` directory containing `html` and `css`, and everywhere else `Markdown` and `Jinja2` templates that make this all hang together.

### The first snag

So obviously the `Jinaja2` templates are only for creating `html` files to upload to the blog, but for the `Markdown` files, I would like some files to go on the blog, others not, some on Medium, others not, etc.
I can also easily imagine a future in which I would like to add additional channels, so I needed a quick and easy way to drop some metadata in the Markdown. [`Gatsby`](https://www.gatsbyjs.org/) seems to have adopted the standard of hydrating a page with a `---`. Fortunately, Markdown appears to accept this symbol without any parse errors, so I'm happy to keep the standard. Inside the `---`, I'll drop some Yaml text. Problem solved!

Let's write some code to parse such a file.
