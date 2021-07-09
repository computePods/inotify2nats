# This is the ComputePods inotify to NATS (cpinotify) tool

# This tool reads in a cpinotifyConfig.yaml file describing the NATS
# server to be notified as well as the directories to be watched using the
# Linux filesystem inotify system.

# The configuration file allows collections of different directories to be
# monitored as well as which NATS channels to be informed of any changes
# detected.

import asyncio
import argparse
import logging
import signal
import traceback

import cpinotify.loadConfiguration
import cpinotify.recursivewatch
from .natsClient import NatsClient

argparser = argparse.ArgumentParser(description="Listen for inotify events and forward them onto a NATS server")
argparser.add_argument('-b', '--base-dir',
  help="Specify the base directory for all releative paths")
argparser.add_argument('-c', '--config',
  help="Load configuration from file")
argparser.add_argument('-P', '--port',
  help="The NATs server's port")
argparser.add_argument('-H', '--host',
  help="The NATs server's host")
argparser.add_argument('-v', '--verbose',
  action=argparse.BooleanOptionalAction,
  help="Report additional information about what is happening")

cliArgs = argparser.parse_args()

#logging.basicConfig(filename='inotify2nats.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

class SignalException(Exception):
  def __init__(self, message):
    super(SignalException, self).__init__(message)

def signalHandler(signum, frame) :
  msg = "SignalHandler: Caught signal {}".format(signum)
  logging.info(msg)
  raise SignalException(msg)

signal.signal(signal.SIGTERM, signalHandler)
signal.signal(signal.SIGHUP, signalHandler)

async def main(config) :
  natsClient = NatsClient("cpLogger")
  await natsClient.connectToServers()

  await  cpinotify.recursivewatch.watchForInotifyEvents(config['watches'], natsClient)


def cli() :
  configFile = './cpinotifyConfig.yaml'
  if cliArgs.config  : configFile = cliArgs.config
  verbose    = False
  if cliArgs.verbose : verbose = cliArgs.verbose
  config = cpinotify.loadConfiguration.loadConfig(configFile, verbose)

  logging.info("ComputePods inotify2nats starting")
  asyncio.run(main(config))
  logging.info("ComputePods inotify2nats stopping")
