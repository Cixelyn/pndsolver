from tornado import web, ioloop, escape

import base64
import json

import cStringIO
from PIL import Image
from .util import bgr_to_rgb

import logging

from .classifier import classify_orbs
from .solver import solve_board
from .models import Board

import logging
logger = logging.getLogger(__name__)

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

  def _solve_action(self):
    data = self.json_args.get('board')
    logger.info("Solving: %s" % data)
    board = Board(data)
    self.write(json.dumps(solve_board(board)))

  def get(self, action):
    if action == 'capture':
      self._capture_action()

  def post(self, action):
    self.json_args = escape.json_decode(self.request.body);

    if action == 'solve':
      self._solve_action()
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
      (r'/(capture|solve|run)', ApiHandlerFactory(driver)),
      (r'/(.*)', web.StaticFileHandler, {'path': './ui/'})
  ], serve_traceback=True)
  return app


def run_app(app, port):
  logger = logging.getLogger(__name__)
  logger.info("Starting GUI on port %s" % port)

  app.listen(port)
  ioloop.IOLoop.instance().start()


