#!/usr/bin/env python
#
# Python convenience functions for computer engineering
#
# These functions are intended to be used in an interactive Python
# shell (i.e., like a calculator).  To automatically include these
# functions for all Python shells, add the following to ~/.python.start.py:
#
#     import os, sys
#     # Append home directory to PYTHONPATH
#     sys.path.append(os.path.expanduser("~"))
#     from cmpe import *
#
# Alternatively, you can also simply invoke this script and it will
# launch a basic Python interactive shell with these functions available
# in the global namespace.
#
# To update to the latest version of this script, simply run:
#
#     $ curl -O https://raw.github.com/nacase/py-cmpe/master/cmpe.py
#
# Author: Nate Case <nacase@gmail.com>

import math
import urllib
import httplib
import re

def group_str(str,length):
    """Break up a string into groups of specified length, separated by
    spaces.  Right justified."""
    new = ""
    i = length - (len(str) % length)
    for c in str:
        new += c
        i += 1
        if (i % length == 0):
            new += " "
    return new


def rawhex(hexstr):
    """Strip any extra chars off a hex string.  Specifically, the leading
    '0x' and trailing 'L' if they exist."""
    s = hexstr
    if hexstr.startswith("0x"):
        s = s[2:]
    if hexstr.endswith("L"):
        s = s[:-1]
    return s

def int2bin(val,num_bits=0):
    """Convert an integer to a binary string."""
    bits = []
    s = ""
    if num_bits == 0:
        num_bits = len(rawhex(hex(val))) * 4
    for x in range(0,num_bits):
        if (val >> x) & 0x1:
            bits.insert(0, 1)
        else:
            bits.insert(0, 0)

    for bit in bits:
        s = s + "%d" % bit

    return s

def bitrev(val,bits):
    """Return bit-reversed value."""
    binstr = int2bin(val)
    if len(binstr) != bits:
        binstr = "0" * (bits-len(binstr)) + binstr
    revs = ""
    for c in binstr:
        revs = c + revs
    return int(revs, 2)

def hex2bin(hexstr):
    """Convert a hex string byte to binary."""
    hexstr = rawhex(hexstr)
    dec = int(hexstr,16)
    return int2bin(dec)

def bin2int(binstr):
    """Convert a binary string to an integer."""
    return int(binstr, 2)

def bin(binstr):
    """Convert a binary string to an integer."""
    return int(binstr, 2)

def ones(val,bits=32,bitrev=0):
    """Return a list of bit values that are '1' in a given integer."""
    l = []
    for x in range(0,bits):
        if (val & (1 << x)):
            if bitrev:
                l.append(bits-x-1)
            else:
                l.append(x)
    return l

def zeros(val,bits=32,bitrev=0):
    """Return a list of bit values that are '0' in a given integer."""
    l = []
    for x in range(0,bits):
        if not (val & (1 << x)):
            if bitrev:
                l.append(bits-x-1)
            else:
                l.append(x)
    return l

def inspect(val,bitrev=0,num_bits=0):
    """Given an integer, print a string showing it in various forms."""
    binstr = int2bin(val,num_bits)
    bits = len(binstr)
    s = ""
    s += "Decimal\t\t\t:\t%d\n" % val
    s += "Hexadecimal\t\t:\t0x%x\n" % val
    s += "Binary\t\t\t:\t%s\n" % binstr
    s += "\t\t\t:\t"
    for x in range(bits-1,-1,-4):
        if bitrev:
            bitnum = (bits-x-1)
        else:
            bitnum = x
        s += "%2d   " % bitnum 
    s += "\n"
    s += "Binary (grouped)\t:\t %s\n" % group_str(int2bin(val,num_bits),4)
    s += "One bits\t\t:\t%s\n" % ones(val,bits,bitrev)
    s += "Zero bits\t\t:\t%s\n" % zeros(val,bits,bitrev)
    print s,

def rdiv(vcc,r1,r2):
    """Calculate the voltage in between R1 and R2 in a resistor divider.
       R1 is the resistor closest to VCC, R2 is connected to GND."""
    return vcc * (1 - (r1*1.0)/(r1+r2+0.0))

def rms(ppval):
    """Calculate RMS equivalent value for the given peak-to-peak value."""
    return ppval * (1/math.sqrt(2.0))

def pk(rmsval):
    """Calculate peak equivalent value for the given RMS value."""
    return rmsval / (1/math.sqrt(2.0))

def pp(rmsval):
    """Calculate peak-to-peak equivalent value for the given RMS value."""
    return pk(rmsval) * 2

def dbgain(mult):
    """For a given multiplier (mult:1), calculate the equivalent gain
    in dB.  For example, 9:1 gain is about 19 dB."""
    return 20 * math.log(mult*1.0, 10)

def ampgain(dB):
    """For a given dB gain value, calculate the equivalent Output:Input
    ratio.  For example, a gain of 19 dB is roughly 9x (9:1)."""
    return 10 ** (dB/20.0)

# Byte-swapping.  Inspired by Linux's swab.h style

def swab16(x):
    """Swap bytes in 16-bit value.  e.g., swab16(0x1234) = 0x3412"""
    return ((((x & 0x00ff) << 8) |((x & 0xff00) >> 8)))

def swab32(x):
    """Swap bytes in 32-bit value.  e.g., swab32(0x12345678) = 0x78563412"""
    return (( \
        ((x & 0x000000ff) << 24) |
        ((x & 0x0000ff00) <<  8) |
        ((x & 0x00ff0000) >>  8) |
        ((x & 0xff000000) >> 24)))

def swab64(x):
    """Swap bytes in 64-bit value.
       e.g., swab64(0x123456789abcdef0) = 0xf0debc9a78563412"""
    return (( \
        ((x & 0x00000000000000ff) << 56) |
        ((x & 0x000000000000ff00) << 40) |
        ((x & 0x0000000000ff0000) << 24) |
        ((x & 0x00000000ff000000) <<  8) |
        ((x & 0x000000ff00000000) >>  8) |
        ((x & 0x0000ff0000000000) >> 24) |
        ((x & 0x00ff000000000000) >> 40) |
        ((x & 0xff00000000000000) >> 56)))

def swah32(x):
    """Swap half-words in a 32-bit value.
        e.g., swah32(0x12345678) = 0x56781234"""
    return (((x & 0x0000ffff) << 16) | ((x & 0xffff0000) >> 16))

def swahb32(x):
    """Swap bytes within half-words.
        e.g., swahb32(0x12345678) = 0x34127856"""
    return (((x & 0x00ff00ff) << 8) | ((x & 0xff00ff00) >> 8))

def gc(s):
    """Pass string to google calculator and return result string.  This
    is most useful for unit conversions; i.e., '123 inches in cm'."""
    q = urllib.urlencode({'q': s})
    conn = httplib.HTTPConnection("www.google.com")
    conn.request("GET", "/search?%s" % q)
    resp = conn.getresponse()
    data = resp.read()

    #r = re.compile(r"<h2 class=r style=.font-size:138%.><b>(.+)</b></h2>")
    # NAC: Updated from google changes in November 2011
    r = re.compile(r"<h2 class=.?r.? .*style=.font-size:138%.>(<b>)?(.+)(</b>)?</h2>", re.DOTALL)
    m = r.search(data)
    if m:
        return m.group(2).replace("\xa0", ""). \
                replace('<font size=-2> </font>', ''). \
                replace('\n', ' '). \
                replace('  ', ''). \
                replace(' &#215; 10<sup>','e').replace('</sup>', '')

    return "Result not found"

if __name__ == "__main__":
    """Start an interactive shell with all functions available.  Normally,
    it's better to import this module from your own interactive shell.
    But do something reasonable when invoking this file directly."""
    import readline
    import code
    import pydoc
    vars = globals().copy()
    vars.update(locals())
    # Show some help
    print pydoc.render_doc("cmpe")
    shell = code.InteractiveConsole(vars)
    shell.interact()
