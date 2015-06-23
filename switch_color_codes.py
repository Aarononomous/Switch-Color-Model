import sublime, sublimeplugin, re

class SwitchColorCodes(sublimeplugin.TextCommand):
  hex3 = re.compile('^#([a-f\d])([a-f\d])([a-f\d])$', re.IGNORECASE)
  hex6 = re.compile('^#([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])$', re.IGNORECASE)
  # rgb  = re.compile('^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$')
  # rgba = re.compile('^rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*1\)$')
  # hsl  = re.compile('^hsl\((\d{1,3}),\s*(\d{1,3})%,\s*(\d{1,3})%\)$')
  # hsla = re.compile('^hsla\((\d{1,3}),\s*(\d{1,3})%,\s*(\d{1,3})%,\s*1\)$')

  def run(self, view, args):
    for region in view.sel():
      swapped = switch(view.substr(region))
      view.replace(region, swapped)

  def switch(s):
    if hex3.match(s):
      colors = hex3.findall(s)
      r = int(colors[0], 16) * 17
      g = int(colors[1], 16) * 17
      b = int(colors[2], 16) * 17
      return to6Hex(r,g,b)
    elif hex6.match(s):
      colors = hex3.findall(s)
      r = int(colors[0] + colors[1])
      g = int(colors[2] + colors[3])
      b = int(colors[4] + colors[5])
      return to3Hex(hex6.findall(s))
    else: return s

  def toHex(n):
    hex  = list('0123456789abcdef')
    if n < 16: return hex[n]
    else: return toHex(n//16) + hex[n % 16]

  def to3Hex(r,g,b):
    if r%17 == 0 and g&17 == 0 and b%17 == 0:
      return '#' + toHex(r/17) + toHex(g/17) + toHex(b/17)
    else return to6Hex(r,g,b)

  def to6Hex(r,g,b):
    return '#' + toHex(r) + toHex(g) + toHex(b)

  # def toRGB(r,g,b):
  #   return 'rgb(' + r + ',' + g + ',' + b + ")"

  # def toRGBA(r,g,b):
  #   return 'rgba(' + r + ',' + g + ',' + b + ",1)"

  # def toHSL(r,g,b):
  #   # Convert to range [0,1)
  #   R = r / float(255)
  #   G = g / float(255)
  #   B = b / float(255)
  #   min = min(R,G,B)
  #   max = max(R,G,B)
  #   # Luminance
  #   L = (min + max)/2.0
  #   l = round(L * 100)
  #   # Saturation
  #   if L < 0.5: S = (max-min)/(max+min)
  #   else: S = (max-min)/(2.0-max-min)
  #   s = round(S * 100)
  #   # Hue
  #   if R == max: H = (G-B)/(max-min)
  #   elif G == max: H = 2.0 + (B-R)/(max-min)
  #   else: H = 4.0 + (R-G)/(max-min)
  #   h = round(H * 60 + 360) % 360

  #   return 'hsl(' + h + ',' + s + '%,' + l + '%)'

  # def toHSLA(r,g,b):
  #   # Convert to range [0,1)
  #   R = r / float(255)
  #   G = g / float(255)
  #   B = b / float(255)
  #   min = min(R,G,B)
  #   max = max(R,G,B)
  #   # Luminance
  #   L = (min + max)/2.0
  #   l = round(L * 100)
  #   # Saturation
  #   if L < 0.5: S = (max-min)/(max+min)
  #   else: S = (max-min)/(2.0-max-min)
  #   s = round(S * 100)
  #   # Hue
  #   if R == max: H = (G-B)/(max-min)
  #   elif G == max: H = 2.0 + (B-R)/(max-min)
  #   else: H = 4.0 + (R-G)/(max-min)
  #   h = round(H * 60 + 360) % 360

  #   return 'hsla(' + h + ',' + s + '%,' + l + '%,1)'
