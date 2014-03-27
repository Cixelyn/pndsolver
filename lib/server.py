from tornado import web, ioloop

import base64
import json

import cStringIO
from PIL import Image
from .util import bgr_to_rgb

import logging

from .classifier import classify_orbs


class ApiHandler(web.RequestHandler):

  def set_driver(self, driver):
    self.driver = driver

  def _capture_action(self):
      frame = self.driver.capture()
      board = classify_orbs(frame)

      im = Image.fromarray(bgr_to_rgb(frame))
      buf = cStringIO.StringIO()
      im.save(buf, format='png')
      buf.seek(0)

      self.set_header('Content-Type', 'application/json')
      data = {
          'board': board.data,
          'frame': 'data:image/png;base64,' + base64.standard_b64encode(buf.read())
      }
      self.write(json.dumps(data))

  def _run_action(self):
    self.write('not implemented')

  def get(self, action):
    if action == 'capture':
      self._capture_action()
    elif action == 'run':
      self._run_action()


def ApiHandlerFactory(driver):
  def wrapper(*args, **kwargs):
    c = ApiHandler(*args, **kwargs)
    c.set_driver(driver)
    return c
  return wrapper


def create_app(driver):
  app = web.Application([
      (r'/(capture|run)', ApiHandlerFactory(driver)),
      (r'/(.*)', web.StaticFileHandler, {'path': './ui/'})
  ])
  return app


def run_app(app, port):
  logger = logging.getLogger(__name__)
  logger.info("Starting GUI on port %s" % port)

  app.listen(port)
  ioloop.IOLoop.instance().start()


