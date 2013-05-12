# Build
*Project layout, edit templates and manage Google spreadsheet, tweak CSS, and take a peek at
the Javascript app.*

Now that you've created a new project, let's look at how Tarbell projects are constructed.

## Project layout

<div class="row-fluid">

<div class="span7"> 
<p>A Tarbell template project directory structure looks like this:</p>

<ul class="directories">
<li><p><code>config.py</code>: Configuration file. Required to detect the project.</p></li>
<li><p><code>secrets.py</code>: Set <code>GOOGLE_AUTH</code> variable to configure authentication. Not tracked by Git.</p></li>
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

Every file that ends in `.html` in `projectname/templates` will be published to
`projectname/TEMPLATENAME.html` and can be previewed at <a href="http://localhost:5000/projectname/TEMPLATENAME.html">http://localhost:5000/projectname/TEMPLATENAME.html</a>.

### Template basics

<div class="row-fluid">

<div class="span8"> 
<p>Tarbell uses <a href="http://jinja.pocoo.org/docs/">Jinja2</a> for templating and supports
all Jinja2 features.</p>

<p>A basic template looks like:</p>

<pre><code class="django">&#123;% extends '_base.html' %&#125;

&#123;% block css %&#125;
&#123;&#123; super() &#125;&#125; &#123;# Load base styles #&#125;
&lt;link rel="stylesheet" type="text/css"
    href="&#123;&#123; static_url('MYPROJECT', '/css/style.css') &#125;&#125;" /&gt;
&#123;% endblock css %&#125;

&#123;% block content %&#125;
&lt;h1&gt;&#123;&#123; title &#125;&#125;&lt;/h1&gt;
&lt;p class="credit"&gt;&#123;&#123; credit &#125;&#125;&lt;/p&gt;
&#123;&#123; body|process_text &#125;&#125;
&#123;% endblock content %&#125;
</code></pre>

</div>

<div class="span4 aside">
    <h2><i class="icon icon-question-sign"></i> What's <code>_base.html</code>?</h2> 
    <p>The Tarbell template comes with a base template file that sets up some simple blocks and manages Javascript app loading.</p>
</div>

</div>

#### The `static_url()` template function

The `static_url(projectname, path)` function constructs the path to an asset 
stored under `projectname/static` based on the project's output URL.

### Working with Google spreadsheets: The "values" worksheet

The <strong>values</strong> worksheet must have "key" and
"value" columns. These key-value pairs will be provided as global
variables to templates. So if there's a row with a key column value
of "foo" and a value of "bar", <code>{{ foo }}</code> in a template will print
<code>bar</code>.

### Working with Google spreadsheets: Other worksheets

Other worksheets can hold freeform data, namespaced by the
worksheet name. Unlike the <strong>values</strong> worksheet, data in these
worksheets can be accessed by iterating through a list or, if a column named
"key" is present, by reference to the value in that column. Some examples with 
a worksheet named <strong>updates</strong> should help make this clear.

#### A worksheet called "updates"

<table class="table">
    <tr>
        <th>key&nbsp;&nbsp;&nbsp;&nbsp;</th>
        <th>title&nbsp;&nbsp;&nbsp;&nbsp;</th>
        <th>date&nbsp;&nbsp;&nbsp;&nbsp;</th>
        <th>url&nbsp;&nbsp;&nbsp;&nbsp;</th>
    </tr>
    <tr>
        <td>hadiya</td>
        <td>Hadiya's friends</td>
        <td>05-05-2013</td>
        <td>http://graphics.chicagotribune.com/hadiyas-friends</td>
    </tr>
    <tr>
        <td>grace</td>
        <td>His Saving Grace</td>
        <td>02-14-2013</td>
        <td>http://graphics.chicagotribune.com/grace</td>
    </tr>
</table>

<h3>Get worksheet values in template</h3>

<p>The worksheet will be passed to your context as an iterable list, with each
column in the worksheet representing a separate item in the context dictionary. So in your
template, the following code displays the contents of each row in your spreadsheet:</p>

<pre><code class="django">&#123;% for row in updates %&#125;
&lt;p&gt; &lt;a href="&#123;&#123; row.url &#125;&#125;"&gt;&#123;&#123; row.title &#125;&#125;&lt;/a&gt; &lt;/p&gt; 
&#123;% endfor %&#125;</code></pre>

<h3>Directly accessing a row</h3>

<p>If there's a header named "key" that contains only unique, simple string values
we can directly access individual rows in that worksheet:</p>

<pre><code class="django">&lt;p&gt; &lt;a href="&#123;&#123; updates.grace.url &#125;&#125;"&gt;&#123;&#123; updates.grace.title &#125;&#125;&lt;/a&gt; &lt;/p&gt;</code></pre>

## Editing Javascript app

Every project comes with a barebones Javascript app in `projectname/static/js/app.js`.

The app uses RequireJS and provides Backbone, jQuery, and Underscore libraries by
default.

Wrap your app code in a `require(['dependency', ...], function(DepObj) { ... })`
call to include necessary libraries and modules. 

<pre><code class="javascript">// Additional RequireJS configuration
require.config( {
    paths: {
        moment: '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min',
    },
} );

// Start our project's app
require([ 'jquery', 'base/views/NavigationView', 'moment' ],
function($, NavigationView, moment) {
    console.log("Creating navigation view");
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: 'Tarbell Readme', url: '#top' },
    }).render();

    console.log("Demonstrating momentJS:");
    console.log(new moment());
});
</code></pre>
