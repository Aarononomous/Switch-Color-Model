import sublime, sublime_plugin, re

hex3 = re.compile('^#([a-f\d])([a-f\d])([a-f\d])$', re.IGNORECASE)
hex6 = re.compile('^#([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])$', re.IGNORECASE)
rgb  = re.compile('^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$')
rgba = re.compile('^rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*1\)$')
# hsl  = re.compile('^hsl\((\d{1,3}),\s*(\d{1,3})%,\s*(\d{1,3})%\)$')
# hsla = re.compile('^hsla\((\d{1,3}),\s*(\d{1,3})%,\s*(\d{1,3})%,\s*1\)$')

def switch(s):
  if hex3.match(s):
    colors = list(hex3.findall(s)[0])
    r = int(colors[0], 16) * 17
    g = int(colors[1], 16) * 17
    b = int(colors[2], 16) * 17
    return to6Hex(r,g,b)
  elif hex6.match(s):
    colors = list(hex6.findall(s)[0])
    r = int(colors[0] + colors[1], 16)
    g = int(colors[2] + colors[3], 16)
    b = int(colors[4] + colors[5], 16)
    return toRGB(r,g,b)
  elif rgb.match(s):
    colors = list(rgb.findall(s)[0])
    r = int(colors[0])
    g = int(colors[1])
    b = int(colors[2])
    if r <= 255 and g <= 255 and b <= 255:
      return toRGBA(r,g,b)
  elif rgba.match(s):
    colors = list(rgba.findall(s)[0])
    r = int(colors[0])
    g = int(colors[1])
    b = int(colors[2])
    if r <= 255 and g <= 255 and b <= 255:
      return to3Hex(r,g,b)
  return s

def toHex(n):
  return "{0:0{1}x}".format(n,2)

def to3Hex(r,g,b):
  if r%17 == 0 and g&17 == 0 and b%17 == 0:
    return '#' + toHex(r//17) + toHex(g//17) + toHex(b//17)
  else: return to6Hex(r,g,b)

def to6Hex(r,g,b):
  return '#' + toHex(r) + toHex(g) + toHex(b)

def toRGB(r,g,b):
  return 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ")"

def toRGBA(r,g,b):
  return 'rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ",1)"

class SwitchColorModelCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    for region in self.view.sel():
      swapped = switch(self.view.substr(region))
      self.view.replace(edit, region, swapped)