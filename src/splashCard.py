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
splashCard.py:  The SplashCard will hide the scene and present a simple message
while the scene is being prepared.

Borrowed some code from Astelix from the Panda3d forum. Thanks Astelix.
"""

from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from config import *

class SplashCard(object):
    '''this class shows up a splash message'''
    #------------------------------------------------------------
    #
    def __init__(self, image, backgroundColor):
        self.loadingimage = OnscreenImage(image, color=(1, 1, 1, 1), scale=.5, parent=aspect2d)
        self.loadingimage.setTransparency(1)
        # this image will be on top of all therefore we use setBin 'fixed' and with the higher sort value
        self.loadingimage.setBin("fixed", 20)

        self.curtain = OnscreenImage('textures/curtain.png', parent=render2d, color=backgroundColor)
        self.curtain.setTransparency(1)
        # this is to set it below the loading panel
        self.curtain.setBin("fixed", 10)

        # the loading panel faders
        self.loadingOut = self.loadingimage.colorInterval(1, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1))
        # the black curtain faders
        self.openCurtain = self.curtain.colorScaleInterval(1, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1))
        for i in range(4):
            base.graphicsEngine.renderFrame()
    #------------------------------------------------------------
    #
    def destroy(self):
        Sequence(self.loadingOut, self.openCurtain).start()
        #Sequence(self.openCurtain).start()
        #self.loadingimage.destroy()
        #self.curtain.destroy()