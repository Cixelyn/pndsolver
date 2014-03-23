# -*- coding: utf-8 -*-

from collections import namedtuple

OrbInfo = namedtuple('OrbData', [
    'name',
    'abbr',
    'termcolor',
    'termchar',
    'drawcolor',
    'huerange',
  ])

ORB_DATA = {
  0x00: OrbInfo(
    name='Blank',
    abbr='.',
    termcolor=16,
    termchar='㊀',
    drawcolor=(0,0,0),
    huerange=None,
  ),
  0x01: OrbInfo(
    name='Fire',
    abbr='r',
    termcolor=196,
    termchar='㊋',
    drawcolor=(252,81,50),
    huerange=(18, 37),
  ),
  0x02: OrbInfo(
    name='Water',
    abbr='b',
    termcolor=68,
    termchar='㊌',
    drawcolor=(66,130,202),
    huerange=(136, 152),
  ),
  0x03: OrbInfo(
    name='Wood',
    abbr='g',
    termcolor=40,
    termchar='㊍',
    drawcolor=(26,168,94),
    huerange=(93, 107),
  ),
  0x04: OrbInfo(
    name='Light',
    abbr='y',
    termcolor=227,
    termchar='㊐',
    drawcolor=(255,238,85),
    huerange=(37, 47),
  ),
  0x05: OrbInfo(
    name='Dark',
    abbr='p',
    termcolor=129,
    termchar='㊊',
    drawcolor=(96,0,119),
    huerange=(200, 214),
  ),
  0x06: OrbInfo(
    name='Heal',
    abbr='h',
    termcolor=211,
    termchar='㊩',
    drawcolor=(238,119,204),
    huerange=(223, 237),
  ),
  0x07: OrbInfo(
    name='Poison',
    abbr='j',
    termcolor=250,
    termchar='㊀',
    drawcolor=(100,100,100),
    huerange=None,
  ),
}