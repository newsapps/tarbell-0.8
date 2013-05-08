from tarbell.app import TarbellSite
import os

site = TarbellSite(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    site.app.run('0.0.0.0')
