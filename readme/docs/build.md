# Build a project

Now that you've created a new project, let's look at how Tarbell projects are constructed. 

## Project layout

A Tarbell project directory structure looks like this:

* `config.py`: Configuration file. Required to detect the project.
* `templates`: The templates directory contains Jinja templates that will be published at `/projectname/TEMPLATENAME.html`.
* `static`: The static directory contains static assets like images, CSS, and Javascript. They are published at `/projectname/FILENAME`.

**What's the difference between static assets and templates?** Static assets are simply served as-is, while templates are provided with context variables and rendered using Jinja.

## Editing templates

## Editing Javascript app
