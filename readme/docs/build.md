# Build
*Manage your Google spreadsheet, edit templates, tweak CSS, and take a peek at
the Javascript app.*

Now that you've created a new project, let's look at how Tarbell projects are constructed.

<h2>Project layout</h2>

<div class="row-fluid">

<div class="span7"> 
<p>A Tarbell template project directory structure lookis like this:</p>

<ul class="directories">
<li><p><code>config.py</code>: Configuration file. Required to detect the project.</p></li>
<li><p><code>templates</code>: The templates directory contains Jinja templates that will be published at <code>/projectname/TEMPLATENAME.html</code>.</p>
    <ul>
        <li><p><code>index.html</code>: A basic template to start building with.</p></li>
    </ul>
</li>
<li><p><code>static</code>: The static directory contains static assets like images, CSS, and Javascript. They are published at <code>/projectname/FILENAME</code>.</p></li>
    <ul>
        <li><p><code>js/app.js</code>: An skeleton Javascript application for your project that is automatically loaded by base template.</p></li>
        <li><p><code>css/style.css</code>: An empty stylesheet for your project.</p></li>
    </ul>
</li>
</ul>
</div>

<div class="span4 offset1 aside">
    <h2><i class="icon icon-question-sign"></i> What's the difference between static assets and templates?</h2> 
    <p>Static assets are simply served as-is, while templates are provided with context variables and rendered using Jinja.</p>
</div>

</div>

## Editing templates

## Editing Javascript app
