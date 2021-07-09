import asyncio
import logging
import os
import platform

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def natsClientError(err) :
  logging.error("NatsClient : {err}".format(err=err))

async def natsClientClosedConn() :
  logging.warn("NatsClient : connection to NATS server is now closed.")

async def natsClientReconnected() :
  logging.info("NatsClient : reconnected to NATS server.")

class NatsClient :

  def __init__(self, aContainerName) :
    self.nc = NATS()
    self.containerName = aContainerName
    self.shutdown   = False

  async def connectToServers(self):
    logging.info("NatsClient: connecting to NATS server")
    await self.nc.connect(
      servers=["nats://127.0.0.1:4222"],
      error_cb=natsClientError,
      closed_cb=natsClientClosedConn,
      reconnected_cb=natsClientReconnected
    )

  async def sendMessage(self, aSubject, aMessage) :
    print(f"sending message: {aSubject}:[{aMessage}]")
    await self.nc.publish(aSubject, bytes(aMessage, 'utf-8'))

  async def listenToChannel(self, aChannel, aCallBack) :
    print("listening to channel [{}]".format(aChannel))
    await self.nc.subscribe(aChannel, cb=aCallBack)

  async def closeConnection(self) :
    logging.info("NatsCllient: closing connection")
    # Terminate connection to NATS.
    self.shutdown = True
    await asyncio.sleep(1)
    await self.nc.close()