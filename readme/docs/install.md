# Installing the Tarbell template

Tarbell is a library which powers static sites. It doesn't do much on its own.
To start using Tarbell, we highly recommend using the Tarbell template, which
sets up a publishing workflow using Tarbell.

<pre>
git clone https://github.com/newsapps/tarbell-template
cd tarbell-template
mkvirtualenv tarbell-template
pip install -r requirements.txt
python runserver.py
</pre>

Now visit http://localhost:5000/readme in your browser. You should see the latest
version of this page.

## Amazon S3 setup (optional, highly recommended)

Get your Amazon S3 credentials.

Add some lines to your `~/.bash_profile`:

<pre>
export AWS_ACCESS_KEY_ID="<MY ACCESS KEY ID>"
export AWS_SECRET_ACCESS_KEY="<MY SECRET ACCESS KEY">
</pre>
