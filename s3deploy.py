import sys, os.path
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import mimetypes
import gzip
import tempfile
import logging
import shutil
from optparse import OptionParser
import re
from urllib import quote_plus
from urllib2 import urlopen
import s3config

excludes = r'|'.join([r'.*\.git$'])

def deploy_to_s3(directory, bucket_name, aws_key_id, aws_secret_key, remove=False):
    """
    Deploy a directory to an s3 bucket using parallel uploads.
    """
    directory = directory.rstrip('/')
    connection = S3Connection(aws_key_id, aws_secret_key)
    bucket = connection.get_bucket(bucket_name)
    if remove:
        for x in bucket.list(): bucket.delete_key(x.key)
    
    tempdir = tempfile.mkdtemp('s3deploy')
    for keyname, absolute_path in find_file_paths(directory):
        s3_upload(connection, keyname, absolute_path, bucket, bucket_name, tempdir)

    shutil.rmtree(tempdir,True)
    return True

def s3_upload(connection, keyname, absolute_path, bucket, bucket_name, tempdir):
    """
    Upload a file to s3
    """
    bucket = connection.get_bucket(bucket)

    mimetype = mimetypes.guess_type(absolute_path)
    options = { 'Content-Type' : mimetype[0] }

    # There's a possible race condition if files have the same name
    if mimetype[0] is not None and mimetype[0].startswith('text/'):
        upload = open(absolute_path);
        options['Content-Encoding'] = 'gzip'
        key_parts = keyname.split('/')
        filename = key_parts.pop()
        temp_path = os.path.join(tempdir, filename)
        gzfile = gzip.open(temp_path, 'wb')
        gzfile.write(upload.read())
        gzfile.close()
        absolute_path = temp_path

    k = Key(bucket)
    k.key = keyname
    print "Uploading %s" % keyname
    k.set_contents_from_filename(absolute_path, options, policy='public-read')

    if not keyname.startswith('bootstrap/') and keyname.endswith('.html'):
        param = "http://%s/%s?fbrefresh=CANBEANYTHING" % (bucket_name, keyname)
        print "Refreshing Facebook info for: %s" % param
        fb_url = "http://developers.facebook.com/tools/debug/og/object?q=%s" % quote_plus(param)
        urlopen(fb_url)

def find_file_paths(directory):
    """
    A generator function that recursively finds all files in the upload directory.
    """
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if not re.match(excludes, d)]
        rel_path = os.path.relpath(root, directory)

        for f in files:
            if f.startswith('.'):
                continue
            if rel_path == '.':
                yield (f, os.path.join(root, f))
            else:
                yield (os.path.join(rel_path, f), os.path.join(root, f))

def parse_args():
    parser = OptionParser()
    parser.add_option("-b", "--bucket", dest="bucket_name", action="store", default=None,
                      help="Specify the S3 bucket to which the files should be deployed")
    parser.add_option("-d", "--dir", dest="dir", action="store", default="out",
                      help="Specify the directory which should be copied to the remote bucket. Default 'out'")
    parser.add_option("-r", "--remove", dest="remove", action="store_true", default=False,
                      help="Delete all files from bucket in advance. Use with care.")
    parser.add_option("-k", "--key", dest="key", action="store", default=False,
                      help="AWS access key")
    parser.add_option("-i", "--id", dest="key_id", action="store", default=False,
                      help="AWS access key ID")
    (options, args) = parser.parse_args()
    return options

if __name__ == '__main__':
    opts = parse_args()
    if hasattr(s3config, 'S3CONFIG'):
        if not opts.bucket_name and s3config.S3CONFIG.get('bucket'):
            opts.bucket_name = s3config.S3CONFIG.get('bucket')
        if not opts.key and s3config.S3CONFIG.get('key'):
            opts.key = s3config.S3CONFIG.get('key')
        if not opts.key_id and s3config.S3CONFIG.get('key_id'):
            opts.key_id = s3config.S3CONFIG.get('key_id')
    if not opts.bucket_name:
        raise ValueError("A bucket must be specified.")
    if os.environ.get('AWS_SECRET_ACCESS_KEY') and not opts.key:
        opts.key = os.env.get('AWS_SECRET_ACCESS_KEY')
    if os.environ.get('AWS_ACCESS_KEY_ID') and not opts.key_id:
        opts.key_id = os.env.get('AWS_ACCESS_KEY_ID')
    if not opts.key or not opts.key_id:
        raise ValueError("Error: Access key ID and key value must specified or set as environment variables.")
    print "Deploying to %s" % opts.bucket_name
    deploy_to_s3(opts.dir, opts.bucket_name, opts.key_id, opts.key, opts.remove)
