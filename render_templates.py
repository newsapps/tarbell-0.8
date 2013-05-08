from tarbell.app import TarbellSite
import os
import sys

def render(project=None):
    """Render projects or a specfic project to 'out' directory."""
    site = TarbellSite(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
    site.render_templates(out, project)

if __name__ == "__main__":
    project = None
    if len(sys.argv) > 1:
        project = sys.argv[1]
    render(project)
