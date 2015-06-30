#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re

SETTINGS_FILE = 'SwitchColorModel.sublime-settings'

# regexes for values
h3 = r'\B#([a-f\d])([a-f\d])([a-f\d])\b'
h6 = r'\B#([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])([a-f\d])\b'
rgbInt = r'\brgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)\B'
rgbaInt = r'\brgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*([\d.]+)\)\B'
rgbPct = r'\brgb\(([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)%\)\B'
rgbaPct = r'\brgba\(([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)\)\B'
hslRE = r'\bhsl\(([\d.]+),\s*([\d.]+)%,\s*([\d.]+)%\)\B$'
hslaRE = r'\bhsla\(([\d.]+),\s*([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)\)\B$'

hex3 = re.compile(h3, re.IGNORECASE)
hex6 = re.compile(h6, re.IGNORECASE)
rgb  = re.compile(rgbInt)
rgba = re.compile(rgbaInt)
rgbP  = re.compile(rgbPct)
rgbaP = re.compile(rgbaPct)
hsl  = re.compile(hslRE)
hsla = re.compile(hslaRE)
regexes = re.compile(h3+'|'+h6+'|'+rgbInt+'|'+rgbaInt+'|'+rgbPct+'|'+rgbaPct+'|'+hslRE+'|'+hslaRE)

def switch(match):
    s = match.group()
    if hex3.match(s):
        print('hex3')
        return switchHex3(s)
    elif hex6.match(s):
        print('hex6')
        return switchHex6(s)
    elif rgb.match(s):
        print('rgb')
        return switchRGBInt(s)
    elif rgba.match(s):
        print('rgba')
        return switchRGBAInt(s)
    elif rgbP.match(s):
        print('rgbP')
        return switchRGBPct(s)
    elif rgbaP.match(s):
        print('rgbaP')
        return switchRGBAPct(s)
    elif hsl.match(s):
        print('hsl')
        return switchHSL(s)
    elif hsla.match(s):
        print('hsla')
        return switchHSLA(s)
    else:
        return s

def switchHex3(s):
    colors = list(hex3.findall(s)[0])
    r = int(colors[0], 16) * 17
    g = int(colors[1], 16) * 17
    b = int(colors[2], 16) * 17
    return to6Hex(r,g,b)

def switchHex6(s):
    colors = list(hex6.findall(s)[0])
    r = int(colors[0] + colors[1], 16)
    g = int(colors[2] + colors[3], 16)
    b = int(colors[4] + colors[5], 16)
    return toRGBInt(r,g,b)

def switchRGBInt(s):
    colors = list(rgb.findall(s)[0])
    r = int(colors[0])
    g = int(colors[1])
    b = int(colors[2])
    if r <= 255 and g <= 255 and b <= 255:
        return toRGBAInt(r,g,b,1.0)
    else:
        return s

def switchRGBAInt(s):
    colors = list(rgba.findall(s)[0])
    r = int(colors[0])
    g = int(colors[1])
    b = int(colors[2])
    a = float(colors[3])
    if a < 1.0:
        return toRGBAPct(r,g,b,a)
    if r <= 255 and g <= 255 and b <= 255:
        return toRGBPct(r,g,b)
    else:
        return s

def switchRGBPct(s):
    colors = list(rgbP.findall(s)[0])
    r = float(colors[0]) * 255 / 100
    g = float(colors[1]) * 255 / 100
    b = float(colors[2]) * 255 / 100
    r,g,b = round(r), round(g), round(b)
    print(r,g,b)
    if r <= 255 and g <= 255 and b <= 255:
        return toRGBAPct(r,g,b,1.0)
    else:
        return s

def switchRGBAPct(s):
    colors = list(rgbaP.findall(s)[0])
    r = float(colors[0]) * 255 / 100
    g = float(colors[1]) * 255 / 100
    b = float(colors[2]) * 255 / 100
    a = float(colors[3])
    r,g,b = round(r), round(g), round(b)
    print("rgbap:",r,g,b,a)
    if a < 1.0:
        return toHSLA(r,g,b,a)
    if r <= 255 and g <= 255 and b <= 255:
        return toHSL(r,g,b)
    else:
        return s

def switchHSL(s):
    colors = list(hsl.findall(s)[0])
    h = float(colors[0])
    s = float(colors[1])
    l = float(colors[2])
    r,g,b = HSLtoRGB(h,s,l)
    r,g,b = round(r), round(g), round(b)
    if r <= 255 and g <= 255 and b <= 255:
        return toHSLA(r,g,b,1.0)
    else:
        return s

def switchHSLA(s):
    colors = list(hsla.findall(s)[0])
    h = float(colors[0])
    s = float(colors[1])
    l = float(colors[2])
    a = float(colors[3])
    r,g,b = HSLtoRGB(h,s,l)
    r,g,b = round(r), round(g), round(b)
    if a < 1.0:
        return toRGBAInt(r,g,b,a)
    if r <= 255 and g <= 255 and b <= 255:
        return to3Hex(r,g,b)
    else:
        return s

def HSLtoRGB(h,s,l):
    # normalize hsl values
    H,S,L = h/360, s/100, l/100
    # create some temp variables
    if L < 0.5:
        temp1 = L*(1+S)
    else:
        temp1 = L+S-(L*S)
    temp2 = 2*L-temp1
    # create temp rgb values
    tempR = H + (1/3)
    tempG = H
    tempB = H - (1/3)
    tempR, tempG, tempB = (tempR+1)%1, (tempG+1)%1, (tempB+1)%1
    print("temps ", temp1, temp2)
    print("temps ", tempR, tempG, tempB)
    # tests for rgb vals
    if tempR < (1/6):
        R = temp2+((temp1-temp2)*6*tempR)
    elif tempR < (1/2):
        R = temp1
    elif tempR < (2/3):
        R = temp2+((temp1-temp2)*6*((2/3)-tempR))
    else:
        R = temp2
    print("R:", R)
    if tempG < (1/6):
        G = temp2+(temp1-temp2)*6*tempG
    elif tempG < (1/2):
        G = temp1
    elif tempG < (2/3):
        G = temp2+(temp1-temp2)*6*((2/3)-tempG)
    else:
        G = temp2
    if tempB < (1/6):
        B = temp2+(temp1-temp2)*6*tempB
    elif tempB < (1/2):
        B = temp1
    elif tempB < (2/3):
        B = temp2+(temp1-temp2)*6*((2/3)-tempB)
    else:
        B = temp2
    R,G,B = round(255*R), round(255*G), round(255*B)
    print(R,G,B)
    return (R,G,B)

def RGBtoHSL(r,g,b):
    # normalize rgb values
    R,G,B = r/255, g/255, b/255
    # luminiance
    mini = min(R,G,B)
    print("min: " + str(mini))
    maxi = max(R,G,B)
    print("max: " + str(maxi))
    L = (maxi+mini)/2
    # check for gray -- avoid division by zero
    if (mini == maxi):
        return (0,0,L*100)
    # saturation
    if L < 0.5:
        S = (maxi-mini)/(maxi+mini)
    else:
        S = (maxi-mini)/(2.0-maxi-mini)
    # hue
    if R == maxi:
        H = (G-B)/(maxi-mini)
    elif G == maxi:
        H = Hue = 2.0 + (B-R)/(maxi-mini)
    else: # B == maxi
        H = 4.0 + (R-G)/(maxi-mini)
    H = H * 60
    H = (H + 360) % 360
    S,L = S*100, L*100
    return (H,S,L)

def toH(i):
    return list('0123456789abcdef')[i]

def toH2(i):
    return '{0:0{1}x}'.format(i,2)

def toPct(f):
    # Max four digits after decimal point, but as few as possible
    return '{:.4f}'.format(f).rstrip('0').rstrip('.')

def to3Hex(r,g,b):
    if r%17 == 0 and g%17 == 0 and b%17 == 0:
        return '#' + toH(r//17) + toH(g//17) + toH(b//17)
    else:
        return to6Hex(r,g,b)

def to6Hex(r,g,b):
    return '#' + toH2(r) + toH2(g) + toH2(b)

def toRGBInt(r,g,b):
    return 'rgb('+str(r)+','+str(g)+','+str(b)+')'

def toRGBAInt(r,g,b,a):
    return 'rgba('+str(r)+','+str(g)+','+str(b)+','+toPct(a)+')'

def toRGBPct(r,g,b):
    return 'rgb('+toPct(r/255*100)+'%,'+toPct(g/255*100)+'%,'+toPct(b/255*100)+'%)'

def toRGBAPct(r,g,b,a):
    return 'rgba('+toPct(r/255*100)+'%,'+toPct(g/255*100)+'%,'+toPct(b/255*100)+'%,'+toPct(a)+')'

def toHSL(r,g,b):
    h,s,l = RGBtoHSL(r,g,b)
    return 'hsl('+toPct(h)+','+toPct(s)+'%,'+toPct(l)+'%)'

def toHSLA(r,g,b,a):
    h,s,l = RGBtoHSL(r,g,b)
    return 'hsla('+toPct(h)+','+toPct(s)+'%,'+toPct(l)+'%,'+toPct(a)+')'

class SwitchColorModelCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings(SETTINGS_FILE)

        for region in self.view.sel():
            if region.empty():
                # use the entire line containing the selection(s) or cursor(s)
                region = self.view.full_line(region)
            text = self.view.substr(region)
            text = regexes.sub(switch, text)
            self.view.replace(edit, region, text)

