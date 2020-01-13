# Blog

This is the official source content for all content posted to christophernbyerg.com and associated channels.

My sincere hope here is both document my skills, share knowledge and generally make the world a better place.

Thanks for stopping by!

## About repo

You will find two main directories:

1. `automation` is a set of python scripts that make this all happen seamlessly
2. `content` which is where the actual blog content goes

Additionally, if you run this on your machine, it may create a temporary `build` directory for staging purposes.

## Why not use some other framework

I looked around for a bit and determined there really wasn't anything that cleanly fit what I wanted to do. My objectives were:

1. Blog about stuff as Github flavored Markdown
2. Easily turn that into a blog to that will be hosted in S3
3. Easily cross post any articles I want into other channels (Medium and perhaps others)
4. Automate everything that isn't me writing Markdown or checking code into Github as a CD pipeline

There were a bunch of projects, particularly Gatsby, that looked great in some ways but didn't really have what I had in mind as a clear use case. I thought about it for a bit and decided it wouldn't be that hard to just put something together myself. If this sounds like something you might need, send me a note. Your obviosuly welcome to use the code, but if it's simple enough, I might try to make this friendlier for others who need something similar.

## Developer Dependencies

- Flask
- jinja2
- py-gfm
- pyyaml
