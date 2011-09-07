#!/usr/bin/python

from cli.log import LoggingApp
from insulaudit import core
from pprint import pprint

"""
Very rough.
"""



from console import Subcommand

class QuxApp(Subcommand):
  """Qux Does several special things"""
  name = "qux"
class FuxApp(Subcommand):
  """Fux is accidently different."""
  name = "fux"
class BuxApp(Subcommand):
  """Bux seems special, but it's a trick."""
  name = "bux"

# core
class Session(core.Loggable):
  """A session with a serial device is composed of a file like processing
  object (eg a link), and a handler representing the context controlling the
  link.

  """
  link   = None
  handle = None
  def __init__(self, link, handle):
    self.link    = link
    self.handler = handle
    self.getLog( )

from console import Command

# console
class FlowCommand(Subcommand):
  def __init__(self, flow, **kwds):
    name = kwds.pop('name', flow.__class__.__name__)
    super(type(self), self).__init__(**kwds)
    self.Flow = flow
    
  def main(self, app):
    link    = Link(app.options.port)
    session = Session(link, self)
    flow    = self.Flow(session)
    for F in self.flow( ):
      F(session)


# console, (command, 
class LinkCommand(Command):
  """Processes flows."""
  def __init__(self, **kwds):
    super(type(self), self).__init__( )
    for Flow in self.getFlows( ):
      self.addFlow(Flow)

  def getFlows(self):
    """Give subclasses an opportunity to advertise their own flows."""
    return [ ]

  def subcommand_manufacturer(self, flow):
    return FlowCommand(flow)

  def setup(self, parser):
    setup_device_options(parser)

  def pre_run(self, handler):
    super(type(self), self).pre_run( )
    self.command = self.flows[app.params.command]
    
  def main(self, app):
    self.command.main(self.session)
    


class ScanningDevice(LinkCommand):
  pass

def get_devices():
  devices = [ ]
  a = Command('AAA', [ FuxApp, QuxApp, BuxApp ] )
  b = Command('BBB', [ FuxApp, QuxApp, BuxApp ] )
  return [ a, b ]

from console.utils import setup_device_options, setup_global_options, GlobalOptions

#from console import Application as ConsoleApp
#class ConsoleApp(LoggingApp, GlobalOptions):

class Application(LoggingApp, GlobalOptions):
  """Test Hello World
  """
  name = "insulaudit"
  devices = { }
  
  def __init__(self):
    super(type(self), self).__init__( )
  def setup(self):
    # just after wrapping argument during __call__
    super(type(self), self).setup( )
    #GlobalOptions.setup(self)
    #super(LoggingApp, self).setup( )
    #GlobalOptions.setup(self)
    #self.add_param("bar", help="fake option", action='store_true')
    setup_global_options(self.argparser)
    self.commands = self.argparser.add_subparsers(dest='device', help='fake help on this command')

    self.setup_commands( )
  def pre_run(self):
    # called just before main, updates params, parses args
    super(type(self), self).pre_run()
    #GlobalOptions.pre_run(self)
    #pprint(self.__dict__)
    #LoggingApp.pre_run(self)
    #super(LoggingApp, self).pre_run( )
    device  = self.devices[self.params.device]
    if callable(device.pre_run):
      device.pre_run(self)
    self.selected = device
    #self.selected = command = device.flows[self.params.command]
    #self.selected = command.main

  def main(self):
    self.log.warn("hello world warn")
    self.log.debug("hello world debug")
    self.log.info("hello world info")
    self.log.error("hello world error")
    self.log.critical("hello world critical")
    self.log.fatal("hello world fatal")
    pprint(self.params)
    self.selected.main(self)

    """
class Application(ConsoleApp):
  name = "insulaudit"
    """

  def setup_commands(self):
    for dev in get_devices():
      self.add_device( dev )
    #self.foo = self.commands.add_parser('device', help="foo help")
    #self.foo.add_argument('comm', help='free form')
  def add_device(self, device):
    self.devices[device.name] = device
    parser = self.commands.add_parser(device.name, help=device.help())
    device.setup(parser)

    

if __name__ == '__main__':
  app = Application()
  app.run( )

#####
# EOF
