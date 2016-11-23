#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re

SETTINGS_FILE = 'SwitchCSSColorModel.sublime-settings'


class F:

    """Formats rgba values into output string"""

    # default for hex values is lowercase --
    # change in SwitchColorModel.sublime-settings
    lower = False

    # helper methods
    def to_h(i):
        # one-digit hex number
        return list('0123456789abcdef')[i]

    def to_h_2(i):
        # two-digit hex number with padding
        return '{0:0{1}x}'.format(i, 2)

    def to_pct(f):
        # Max four digits after decimal point, but as few as possible
        return '{:.4f}'.format(f).rstrip('0').rstrip('.')

    def hsl_to_rgb(h, s, l):
        # normalize hsl values
        H, S, L = h/360, s/100, l/100
        # create some temp variables
        if L < 0.5:
            temp1 = L*(1 + S)
        else:
            temp1 = L + S - L*S
        temp2 = 2*L - temp1
        # create temp rgb values
        tempR = H + (1/3)
        tempG = H
        tempB = H - (1/3)
        tempR, tempG, tempB = (tempR + 1) % 1, (tempG + 1) % 1, (tempB + 1) % 1
        # tests for rgb vals
        if tempR < (1/6):
            R = temp2 + (temp1 - temp2)*6*tempR
        elif tempR < (1/2):
            R = temp1
        elif tempR < (2/3):
            R = temp2 + (temp1 - temp2)*6*((2/3) - tempR)
        else:
            R = temp2
        if tempG < (1/6):
            G = temp2 + (temp1 - temp2)*6*tempG
        elif tempG < (1/2):
            G = temp1
        elif tempG < (2/3):
            G = temp2 + (temp1 - temp2)*6*((2/3) - tempG)
        else:
            G = temp2
        if tempB < (1/6):
            B = temp2 + (temp1 - temp2)*6*tempB
        elif tempB < (1/2):
            B = temp1
        elif tempB < (2/3):
            B = temp2 + (temp1 - temp2)*6*((2/3) - tempB)
        else:
            B = temp2
        R, G, B = round(255*R), round(255*G), round(255*B)
        return (R, G, B)

    def rgb_to_hsl(r, g, b):
        # normalize rgb values
        R, G, B = r/255, g/255, b/255
        # luminiance
        mini = min(R, G, B)
        maxi = max(R, G, B)
        L = (maxi + mini) / 2
        # check for gray -- avoid division by zero
        if (mini == maxi):
            return (0, 0, L*100)
        # saturation
        if L < 0.5:
            S = (maxi - mini) / (maxi + mini)
        else:
            S = (maxi - mini) / (2.0 - maxi - mini)
        # hue
        if R == maxi:
            H = (G - B) / (maxi - mini)
        elif G == maxi:
            H = Hue = 2.0 + (B - R) / (maxi - mini)
        else:  # B == maxi
            H = 4.0 + (R - G) / (maxi - mini)
        H = H * 60
        H = (H + 360) % 360
        S, L = S*100, L*100
        return (H, S, L)

    def hex_3(r, g, b, a):
        if r % 17 == 0 and g % 17 == 0 and b % 17 == 0:
            s = '#' + F.to_h(r//17) + F.to_h(g//17) + F.to_h(b//17)
            return s if F.lower else s.upper()
        else:
            return F.hex_6(r, g, b, 1.0)

    def hex_6(r, g, b, a):
        s = '#' + F.to_h_2(r) + F.to_h_2(g) + F.to_h_2(b)
        return s if F.lower else s.upper()

    def rgb(r, g, b, a):
        return 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'

    def rgba(r, g, b, a):
        return ('rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ',' +
                F.to_pct(a) + ')')

    def rgb_pct(r, g, b, a):
        return ('rgb(' + F.to_pct(r/255*100) + '%,' + F.to_pct(g/255*100) +
                '%,' + F.to_pct(b/255*100) + '%)')

    def rgba_pct(r, g, b, a):
        return ('rgba(' + F.to_pct(r/255*100) + '%,' +
                F.to_pct(g/255*100) + '%,' + F.to_pct(b/255*100) + '%,' +
                F.to_pct(a) + ')')

    def hsl(r, g, b, a):
        h, s, l = F.rgb_to_hsl(r, g, b)
        return ('hsl(' + F.to_pct(h) + ',' + F.to_pct(s) + '%,' +
                F.to_pct(l) + '%)')

    def hsla(r, g, b, a):
        h, s, l = F.rgb_to_hsl(r, g, b)
        return ('hsla(' + F.to_pct(h) + ',' + F.to_pct(s) + '%,' +
                F.to_pct(l) + '%,' + F.to_pct(a) + ')')


class GetRGBA:

    """Extracts RGBA values from a string."""

    def hex_3(s):
        colors = hex_3['re'].findall(s)[0]
        r = int(colors[0], 16) * 17
        g = int(colors[1], 16) * 17
        b = int(colors[2], 16) * 17
        return (r, g, b, 1.0)

    def hex_6(s):
        colors = hex_6['re'].findall(s)[0]
        r = int(colors[0] + colors[1], 16)
        g = int(colors[2] + colors[3], 16)
        b = int(colors[4] + colors[5], 16)
        return (r, g, b, 1.0)

    def rgb(s):
        r, g, b = rgb['re'].findall(s)[0]
        return (int(r), int(g), int(b), 1.0)

    def rgba(s):
        r, g, b, a = rgba['re'].findall(s)[0]
        return (int(r), int(g), int(b), float(a))

    def rgb_pct(s):
        colors = rgb_pct['re'].findall(s)[0]
        r = float(colors[0]) * 255 / 100
        g = float(colors[1]) * 255 / 100
        b = float(colors[2]) * 255 / 100
        r, g, b = round(r), round(g), round(b)
        return (r, g, b, 1.0)

    def rgba_pct(s):
        colors = rgba_pct['re'].findall(s)[0]
        r = float(colors[0]) * 255 / 100
        g = float(colors[1]) * 255 / 100
        b = float(colors[2]) * 255 / 100
        a = float(colors[3])
        r, g, b = round(r), round(g), round(b)
        return (r, g, b, a)

    def hsl(s):
        colors = hsl['re'].findall(s)[0]
        h = float(colors[0])
        s = float(colors[1])
        l = float(colors[2])
        r, g, b = F.hsl_to_rgb(h, s, l)
        r, g, b = round(r), round(g), round(b)
        return (r, g, b, 1.0)

    def hsla(s):
        colors = hsla['re'].findall(s)[0]
        h = float(colors[0])
        s = float(colors[1])
        l = float(colors[2])
        a = float(colors[3])
        r, g, b = F.hsl_to_rgb(h, s, l)
        r, g, b = round(r), round(g), round(b)
        return (r, g, b, a)

# regexes for color models
regexes = {
    'hex_3': r'\B#([a-fA-F\d])([a-fA-F\d])([a-fA-F\d])\b',
    'hex_6': r'\B#([a-fA-F\d])([a-fA-F\d])([a-fA-F\d])([a-fA-F\d])([a-fA-F\d])([a-fA-F\d])',
    'rgb': r'\brgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)',
    'rgba': r'\brgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*([\d.]+)\)',
    'rgb_pct': r'\brgb\(([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)%\)',
    'rgba_pct': r'\brgba\(([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)\)',
    'hsl': r'\bhsl\(([\d.]+),\s*([\d.]+)%,\s*([\d.]+)%\)',
    'hsla': r'\bhsla\(([\d.]+),\s*([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)\)'
}

hex_3 = {'re': re.compile(regexes['hex_3']), 'from': 'hex_3', 'to': 'hex_6'}
hex_6 = {'re': re.compile(regexes['hex_6']), 'from': 'hex_6', 'to': 'rgb'}
rgb = {'re': re.compile(regexes['rgb']), 'from': 'rgb', 'to': 'rgba'}
rgba = {'re': re.compile(regexes['rgba']), 'from': 'rgba', 'to': 'rgb_pct'}
rgb_pct = {
    're': re.compile(regexes['rgb_pct']), 'from': 'rgb_pct', 'to': 'rgba_pct'}
rgba_pct = {
    're': re.compile(regexes['rgba_pct']), 'from': 'rgba_pct', 'to': 'hsl'}
hsl = {'re': re.compile(regexes['hsl']), 'from': 'hsl', 'to': 'hsla'}
hsla = {'re': re.compile(regexes['hsla']), 'from': 'hsla', 'to': 'hex_3'}

# concatenate regexes to match multiple occurrences per line
color_models_re = ''
for regex in regexes.values():
    color_models_re += regex + '|'
color_models_re = color_models_re[:-1]  # remove final '|'
color_models = re.compile(color_models_re)


class SwitchCssColorModelCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # settings
        settings = self.view.settings().get('SwitchCSSColorModel')
        if settings is None:
            settings = sublime.load_settings(SETTINGS_FILE)

        # set lower/uppercase output for hex values
        F.lower = settings.get('lowercase_hex')

        # set next models as per other settings (alpha, hsl, and rgb%)
        # using this handy chart - upper = true, lower = false, * = self
        #        ahp    ahP    aHp    aHP    Ahp    AhP    AHp    AHP
        #
        # 3H     6H     6H     6H     6H     6H     6H     6H     6H
        # 6H     RGB    RGB    RGB    RGB    RGB    RGB    RGB    RGB
        # RGB    3H     RGB%   HSL    RGB%   RGBA   RGBA   RGBA   RGBA
        # RGBA   *      RGBA%  HSLA   RGBA%  3H     RGB%   HSL    RGB%
        # RGB%   *      3H     *      HSL    *      RGBA%  *      RGBA%
        # RGBA%  *      RGBA   *      HSLA   *      3H     *      HSL
        # HSL    *      *      3H     3H     *      *      HSLA   HSLA
        # HSLA   *      *      RGBA   RGBA   *      *      3H     3H
        #
        # When alpha value < 1
        # RGBA   *      RGBA%  HSLA   RGBA%  *      RGBA%  HSLA   RGBA%
        # RGBA%  *      RGBA   *      HSLA   *      RGBA   *      HSLA
        # HSLA   *      *      RGBA   RGBA   *      *      RGBA   RGBA

        a = settings.get("use_alpha")
        h = settings.get("recognize_hsl")
        p = settings.get("recognize_rgb_percent")

        if not a and not h and not p:
            rgb['to'] = 'hex_3';        rgba['to'] = 'rgba'
            rgb_pct['to'] = 'rgb_pct';  rgba_pct['to'] = 'rgba_pct'
            hsl['to'] = 'hsl';          hsla['to'] = 'hsla'
        elif not a and not h and p:
            rgb['to'] = 'rgb_pct';      rgba['to'] = 'rgba_pct'
            rgb_pct['to'] = 'hex_3';    rgba_pct['to'] = 'rgba'
            hsl['to'] = 'hsl';          hsla['to'] = 'hsla'
        elif not a and h and not p:
            rgb['to'] = 'hsl';          rgba['to'] = 'hsla'
            rgb_pct['to'] = 'rgb_pct';  rgba_pct['to'] = 'rgba_pct'
            hsl['to'] = 'hex_3';        hsla['to'] = 'rgba'
        elif not a and h and p:
            rgb['to'] = 'rgb_pct';      rgba['to'] = 'rgba_pct'
            rgb_pct['to'] = 'hsl';      rgba_pct['to'] = 'hsla'
            hsl['to'] = 'hex_3';        hsla['to'] = 'rgba'
        elif a and not h and not p:
            rgb['to'] = 'rgba';         rgba['to'] = 'hex_3'
            rgb_pct['to'] = 'rgb_pct';  rgba_pct['to'] = 'rgba_pct'
            hsl['to'] = 'hsl';          hsla['to'] = 'hsla'
        elif a and not h and p:
            rgb['to'] = 'rgba';         rgba['to'] = 'rgb_pct'
            rgb_pct['to'] = 'rgba_pct'; rgba_pct['to'] = 'hex_3'
            hsl['to'] = 'hsl';          hsla['to'] = 'hsla'
        elif a and h and not p:
            rgb['to'] = 'rgba';         rgba['to'] = 'hsl'
            rgb_pct['to'] = 'rgb_pct';  rgba_pct['to'] = 'rgba_pct'
            hsl['to'] = 'hsla';         hsla['to'] = 'hex_3'
        elif a and h and p:
            rgb['to'] = 'rgba';         rgba['to'] = 'rgb_pct'
            rgb_pct['to'] = 'rgba_pct'; rgba_pct['to'] = 'hsl'
            hsl['to'] = 'hsla'
            hsla['to'] = 'hex_3'

        for region in self.view.sel():
            if region.empty() or len(self.view.lines(region)) > 1:
                # then use the line containing the selection(s) or cursor(s)
                region = self.view.line(region)
            text = self.view.substr(region)
            text = color_models.sub(self.switch, text)
            self.view.replace(edit, region, text)

    def switch(self, match):
        s = match.group()
        for model in [hex_3, hex_6, rgb, rgba, rgb_pct, rgba_pct, hsl, hsla]:
            if model['re'].match(s):
                r, g, b, a = getattr(GetRGBA, model['from'])(s)
                # check values
                if (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and
                        0.0 <= a <= 1.0):
                    return getattr(F, model['to'])(r, g, b, a)
                else:
                    return s
        # return original string as default
        # TODO: necessary?
        # return s
