from tornado import web, ioloop

import base64
import json

import cStringIO
from PIL import Image
import numpy
from .util import bgr_to_rgb

import logging

from .classifier import classify_orbs


def get_random_image():
  for n in xrange(10):
    a = numpy.random.rand(30,30,3) * 255
    img = Image.fromarray(a.astype('uint8')).convert('RGBA')
    buf = cStringIO.StringIO() 
    img.save(buf, format='png')
    buf.seek(0)
    return buf


class ImageHandler(web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'image/png') 
    self.write(get_random_image().read())


class CaptureHandler(web.RequestHandler):

  def set_driver(self, driver):
    self.driver = driver

  def get(self):
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


def CaptureHandlerFactory(driver):
  def wrapper(*args, **kwargs):
    c = CaptureHandler(*args, **kwargs)
    c.set_driver(driver)
    return c
  return wrapper


def create_app(driver):
  app = web.Application([
      (r'/capture', CaptureHandlerFactory(driver)),
      (r'/(.*)', web.StaticFileHandler, {'path': './ui/'})
  ])
  return app


def run_app(app, port):
  logger = logging.getLogger(__name__)
  logger.info("Starting GUI on port %s" % port)

  app.listen(port)
  ioloop.IOLoop.instance().start()


