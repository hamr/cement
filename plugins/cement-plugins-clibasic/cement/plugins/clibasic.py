"""
This is a simple plugin to add some basic functionality.
"""

import sys, os
from pkg_resources import get_distribution
import logging

from cement import namespaces
from cement.core.log import get_logger, setup_logging
from cement.core.app_setup import CementCommand, CementPlugin, register_hook, \
                                  register_command, define_hook, register_plugin
from cement.core.options import init_parser

log = get_logger(__name__)

VERSION = '0.2'
REQUIRED_CEMENT_ABI = '20091211'
BANNER = """
cement.plugins.clibasic v%s (abi:%s)
""" % (VERSION, REQUIRED_CEMENT_ABI)
 
@register_plugin() 
class CLIBasicPlugin(CementPlugin):
    def __init__(self):
        CementPlugin.__init__(self,
            label = 'clibasic',
            version = VERSION,
            description = 'Basic CLI Commands for Cement Applications',
            required_abi = REQUIRED_CEMENT_ABI,
            version_banner=BANNER
            )
        
@register_hook()
def global_options_hook(*args, **kwargs):
    """
    Pass back an OptParse object, options will be merged into the global
    options.
    """
    global_options = init_parser()
    global_options.add_option('--debug', action ='store_true', 
        dest='debug', default=None, help='toggle debug output'
    ) 
    global_options.add_option('-C', '--configs', action='store', 
        dest='config_files', default=None, help='config file locations'
    ) 
    return global_options

@register_hook()
def global_post_options_hook(*args, **kwargs):
    """Toggle debug output since we are adding the --debug option via
    this plugin."""
    if namespaces['global'].config['debug']:
        setup_logging('cement', clear_loggers=True)
        setup_logging(namespaces['global'].config['app_module'])
        
    
        
@register_command(name='getconfig')
class GetConfigCommand(CementCommand):
    def run(self):
        try:
            namespace = self.cli_args[1]
        except IndexError:
            self.help()
            sys.exit()
            
        if len(self.cli_args) == 3:
            config_key = self.cli_args[2]
            if namespaces[namespace].config.has_key(config_key):
                print('')
                print('config[%s] => %s' % (config_key, namespaces[namespace].config[config_key]))
                print('')
        else:
            for i in namespaces[namespace].config:
                print("config[%s] => %s" % (i, namespaces[namespace].config[i]))
                
    def help(self):
        print('')
        print('-' * 77) 
        print('')
        print('Print out entire global config dict:')
        print('')
        print('    myapp getconfig global')
        print('')
        print('Or specify an alternate namespace:')
        print('')
        print('    myapp getconfig clibasic')
        print('')
        print('Or specify a config key for just that value:')
        print('')
        print('    myapp getconfig global enabled_plugins')
        print('')
        print('')


@register_command(name='list-plugins')
class ListPluginsCommand(CementCommand):
    def run(self):
        print
        print "%-18s  %-7s  %-50s" % ('plugin', 'ver', 'description')
        print "%-18s  %-7s  %-50s" % ('-'*18, '-'*7, '-'*50)
        
        for plugin in namespaces['global'].config['enabled_plugins']:
            plugin_cls = namespaces[plugin]
            print "%-18s  %-7s  %-50s" % (
                plugin, plugin_cls.version, plugin_cls.description
                )
        print

@register_command(name='list-hooks', is_hidden=True, namespace='clibasic')
class ListHooksCommand(CementCommand):
    def run(self):
        from cement import hooks
        print
        print 'Development Hooks'
        print '-' * 77
        for h in hooks:
            print h
        print
        
@register_command(name='list-hidden-commands')
class ListHiddenCommandsCommand(CementCommand):
    def run(self):
        from cement import commands
        print
        print 'Hidden commands'
        print '-' * 77
        for nam in commands:
            for cmd in commands[nam]:
                if commands[nam][cmd].is_hidden:
                    if nam != 'global':
                        print '%s %s' % (nam, cmd)
                    else:
                        print cmd
                if nam == 'global':
                    print '%s-help' % cmd
                else:
                    print '%s %s-help' % (nam, cmd)
                    
        print