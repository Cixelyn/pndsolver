from tornado import web, ioloop

import cStringIO
from PIL import Image
import numpy


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
  def get(self):
    self.write("hello world")

app = web.Application([
    (r'/image', ImageHandler),
    (r'/(.*)', web.StaticFileHandler, {'path': '.'})
])

if __name__ == '__main__':
  app.listen(9999)
  ioloop.IOLoop.instance().start()

