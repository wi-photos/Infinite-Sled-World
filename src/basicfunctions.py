"""
This file is adapted from the Panda3D Procedural Terrain Engine project (https://github.com/StephenLujan/Panda-3d-Procedural-Terrain-Engine).
Original File Copyright Stephen Lujan. Used for this project with permission.


Zero-Clause BSD
=============

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
"""
basicfunctions.py: This file contains simple useful functions for Panda3d
"""

import time

from direct.gui.OnscreenText import OnscreenText
from direct.stdpy import thread
from panda3d.core import *


# Function returns the width / height ratio of the window or screen
def getScreenRatio():
    props = WindowProperties(base.win.getProperties())
    return float(props.getXSize()) / float(props.getYSize())

# Function to add instructions and other information along either side
def addText(pos, msg, changeable=False, alignLeft=True, scale=0.05):
    x = -getScreenRatio() + 0.03
    if alignLeft:
        align = TextNode.ALeft
    else:
        align = TextNode.ARight
        x *= -1.0
    font = loader.loadFont('fonts/KenneyFutureNarrow.ttf')
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        pos=(x, pos), font=font, align=align, scale=scale,
                        mayChange=changeable)

# Function to put title on the screen.
def addTitle(text):
    addText(-0.95, text, False, False, 0.07)

def showFrame():
    for i in range(4):
        base.graphicsEngine.renderFrame()


def threadContinue(sleeptime, lock):
    lock.release()
    time.sleep(sleeptime)
    lock.acquire()
def screenShot():
    base.screenshot()
    logging.info('screenshot taken.')

def setResolution(x=800, y=600, fullScreen=False):
    wp = WindowProperties()
    wp.setSize(x, y)
    wp.setFullscreen(fullScreen)
    base.win.requestProperties(wp)
