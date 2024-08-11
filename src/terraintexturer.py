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
terraintexturer.py: This file contains the TerrainTexturer class.

The TerrainTexturer handles all textures and or shaders on the terrain and is
generally responsible for the appearance of the terrain.
"""

from config import *
from panda3d.core import *
from terraintexturemap import *

###############################################################################
#   TerrainTexturer
###############################################################################

class TerrainTexturer():
    """Virtual Class"""

    def __init__(self, terrain):
        """initialize"""

        logging.info( "initializing terrain texturer...")
        self.terrain = terrain
        self.load()

    def loadTexture(self, name):
        """A better texture loader"""
        tex = loader.loadTexture('textures/' + name)
        self.defaultFilters(tex)
        return tex

    def defaultFilters(self, texture):
        """Set a texture to use desired default filters."""
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinearMipmapLinear)
        texture.setAnisotropicDegree(2)

    def load(self):
        """Load textures and shaders."""

    def apply(self, input):
        """Apply textures and shaders to the input."""

    def indexToHeight(self, input):
        """Maps a decimal [0.0, 1.0] to [waterHeight, maxHeight]"""
        wh = self.terrain.waterHeight * self.terrain.maxHeight
        return input * (self.terrain.maxHeight - wh) + wh

    def heightToIndex(self, input):
        """Maps the height above sea level to a decimal index."""
        wh = self.terrain.waterHeight * self.terrain.maxHeight
        return (input - wh) / (self.terrain.maxHeight - wh)


###############################################################################
#   MonoTexturer
###############################################################################
class MonoTexturer(TerrainTexturer):
    """Load a single ugly texture onto TerrainTiles."""

    def load(self):
        """single texture"""

        self.ts = TextureStage('ts')
        tex = self.loadTexture("rock.jpg")
        tex.setWrapU(Texture.WMMirror)
        tex.setWrapV(Texture.WMMirror)
        self.monoTexture = tex
    def apply(self, input):
        """Apply textures and shaders to the input."""

        input.setTexture(self.ts, self.monoTexture)
        input.setTexScale(self.ts, 10, 10)

###############################################################################
#   DetailTexturer
###############################################################################

class DetailTexturer(TerrainTexturer):
    """adds a texture + detail texture to TerrainTiles"""

    def load(self):
        self.ts1 = TextureStage('ts2')
        tex = self.loadTexture("snow.jpg")
        tex.setWrapU(Texture.WMMirror)
        tex.setWrapV(Texture.WMMirror)
        self.monoTexture = tex

        self.loadDetail()

    def loadDetail(self):
        self.detailTS = TextureStage('ts')
        tex = self.loadTexture("Detail_COLOR.jpg")
        tex.setWrapU(Texture.WMMirror)
        tex.setWrapV(Texture.WMMirror)
        self.detailTexture = tex
        self.textureBlendMode = self.detailTS.MHeight
        self.detailTS.setMode(self.textureBlendMode)

    def apply(self, input):
        """Apply textures and shaders to the input."""

        input.setTexture(self.ts1, self.monoTexture)
        input.setTexScale(self.ts1, 5, 5)

        input.setTexture(self.detailTS, self.detailTexture)
        input.setTexScale(self.detailTS, 120, 120)


    def setDetailBlendMode(self, num):
        """Set the blending mode of the detail texture."""

        if (not self.detailTexture):
            return
        self.textureBlendMode = num
        #for pos, tile in self.tiles.items():
        #    if tile.detailTS:
        #        tile.detailTS.setMode(self.textureBlendMode)

        self.detailTS.setMode(self.textureBlendMode)

    def incrementDetailBlendMode(self):
        """Set the blending mode of the detail texture."""

        if (not self.detailTexture):
            return
        self.textureBlendMode += 1
        self.setDetailBlendMode(self.textureBlendMode)

    def decrementDetailBlendMode(self):
        """Set the blending mode of the detail texture."""

        if (not self.detailTexture):
            return
        self.textureBlendMode -= 1
        self.setDetailBlendMode(self.textureBlendMode)

###############################################################################
#   ShaderTexturer
###############################################################################
class ShaderTexturer(TerrainTexturer):
    """Adds a shader to TerrainTiles.

    The texturer loads and stores several textures and a detail texture for use
    by the shader in texturing the TerrainTiles.

    """
    def load(self):
        """texture + detail texture"""

        self.loadShader()

    def loadShader(self):
        """Textures based on altitude and slope."""

        logging.info( "loading textures...")
        tex = loader.loadTexture('textures/Material_albedo000.png')
        ts = TextureStage('ts')
        self.terrain.setTexScale(ts, 2)
        tex.setWrapU(Texture.WMMirror)
        tex.setWrapV(Texture.WMMirror)
        self.terrain.setTexture(ts, tex)
        # no lighting or shaders if in browser
        if sys.platform == "emscripten":
            self.terrain.setShaderOff()
            self.terrain.setLightOff()
    
    def apply(self, input):
        """Apply textures and shaders to the input."""
        print("applying")


    def test(self):
        # nothing I want to test here right now
        return