from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")


default_task = ['pycharm_generate','publish']


@init
def initialize(project):
    
    project.version = "0.1.1"
    
    project.build_depends_on('Tkinter', 'ttk', 'networkx')
    project.build_depends_on('matplotlib', 'scipy', 'PIL')
    project.build_depends_on('pympler', 'simpy', 'sklearn')
    project.build_depends_on('collections')
