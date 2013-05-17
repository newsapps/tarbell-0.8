import sys, os.path
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import mimetypes
import gzip
import tempfile
import shutil
from optparse import OptionParser
import re
from urllib import quote_plus
from urllib2 import urlopen
from s3config import S3CONFIG

excludes = r'|'.join([r'.*\.git$'])


def deploy_to_s3(directory, bucket_name, key_id, key):
    """
    Deploy a directory to an s3 bucket using parallel uploads.
    """
    directory = directory.rstrip('/')
    connection = S3Connection(key_id, key)
    bucket = connection.get_bucket(bucket_name)

    tempdir = tempfile.mkdtemp('s3deploy')
    for keyname, absolute_path in find_file_paths(directory):
        s3_upload(connection, keyname, absolute_path, bucket, bucket_name, tempdir)

    shutil.rmtree(tempdir, True)
    return True

def s3_upload(connection, keyname, absolute_path, bucket, bucket_name, tempdir):
    """
    Upload a file to s3
    """
    bucket = connection.get_bucket(bucket)

    mimetype = mimetypes.guess_type(absolute_path)
    options = {'Content-Type': mimetype[0]}

    # There's a possible race condition if files have the same name
    if mimetype[0] is not None and mimetype[0].startswith('text/'):
        upload = open(absolute_path)
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
    parser.add_option("-d", "--dir", dest="dir", action="store", default="out",
                      help="Specify the directory which should be copied to the remote bucket. Default 'out'")
    parser.add_option("-b", "--bucket", dest="bucket", action="store", default=None,
                      help="Specify the S3 bucket to which the files should be deployed")
    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    opts = parse_args()
    bucket = S3CONFIG[opts.bucket]
    print "Deploying to %s" % bucket['bucket']
    deploy_to_s3(opts.dir, bucket['bucket'], bucket['key_id'], bucket['key'])
