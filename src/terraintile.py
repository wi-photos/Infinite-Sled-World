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
terraintile.py: This file contains the terrain tile used by the Terrain class.

TerrainTile is a custom implementation of Panda3d's GeoMipMap.
"""


from collections import deque
from config import *
from panda3d.core import *
from direct.task.Task import Task
#from direct.stdpy import threading2 as threading
import threading
if sys.version_info >= (3, 0):
    import queue
else:
    import Queue
import time



###############################################################################
#   TerrainTile
###############################################################################

class TerrainTile(GeoMipTerrain):
    """TerrainTiles are the building blocks of a terrain."""

    def __init__(self, terrain, x, y):
        """Builds a Tile for the terrain at input coordinates.

        Important settings are used directly from the terrain.
        This allows for easier setting changes, and reduces memory overhead.
        x and y parameters give the appropriate world coordinates of this tile.

        """

        self.terrain = terrain
        self.xOffset = x
        self.yOffset = y
        self.heightMapDetail = 1 # higher means greater detail

        self.name = "ID" + str(terrain.id) + "_X" + str(x) + "_Y" + str(y)
        GeoMipTerrain.__init__(self, name=self.name)

        self.image = PNMImage()


        #self.setAutoFlatten(GeoMipTerrain.AFMOff)
        self.setFocalPoint(self.terrain.focus)
        if sys.platform == "emscripten":
            print("Not setting flatten code because of issues with WEBGL")
        else:
            self.setAutoFlatten(GeoMipTerrain.AFMOff)
        self.getRoot().setPos(x, y, 0)
        if self.terrain.bruteForce:
            GeoMipTerrain.setBruteforce(self, True)
            GeoMipTerrain.setBlockSize(self, self.terrain.heightMapSize * self.heightMapDetail)
        else:
            GeoMipTerrain.setBlockSize(self, self.terrain.blockSize/2)
            #self.setBorderStitching(1)
            self.setNear(self.terrain.near)
            self.setFar(self.terrain.far)


    def update(self):
        """Updates the GeoMip to use the correct LOD on each block."""

        #logging.info("TerrainTile.update()")
        GeoMipTerrain.update(self)

    def updateTask(self, task):
        """Updates the GeoMip to use the correct LOD on each block."""

        self.update()
        return task.again
    def setHeightField(self, filename):
        """Set the GeoMip heightfield from a heightmap image."""

        GeoMipTerrain.setHeightfield(self, filename)

    def generate(self):
        GeoMipTerrain.generate(self)

    def setHeight(self):
        """Sets the height field to match the height map image."""

        self.setHeightField(self.image)

    def makeHeightMap(self):
        """Generate a new heightmap image.

        Panda3d GeoMipMaps require an image from which to build and update
        their height field. This function creates the correct image using the
        tile's position and the Terrain's getHeight() function.

        """

        if SAVED_HEIGHT_MAPS:
            fileName = "maps/height/" + self.name + ".png"
            self.getRoot().setTag('EditableTerrain', '1')
            if self.image.read(Filename(fileName)):
                logging.info( "read heightmap from " + fileName)
                return

        heightMapSize = self.terrain.tileSize * self.heightMapDetail + 1
        self.image = PNMImage(heightMapSize, heightMapSize, 1, 65535)

        ySize = self.image.getYSize() - 1
        getHeight = self.terrain.getHeight
        setGray = self.image.setGray
        xo = self.xOffset
        yo = self.yOffset
        d = self.heightMapDetail

        for x in range(self.image.getXSize()):
            for y in range(ySize + 1):
                height = getHeight(x / d + xo, y / d + yo)
                #  feed pixel into image
                # why is it necessary to invert the y axis I wonder?
                setGray(x, ySize - y, height)
        #self.postProcessImage()
        if SAVED_HEIGHT_MAPS:
            fileName = "maps/height/" + self.name + ".png"
            logging.info( "saving heightmap to " + fileName)
            self.image.write(Filename(fileName))


    def postProcessImage(self):
        """Perform filters and manipulations on the heightmap image."""

        #self.image.gaussianFilter()

    def setWireFrame(self, state):
        self.getRoot().setRenderModeWireframe()

    def makeSlopeMap(self):

        self.slopeMap = PNMImage()
        if SAVED_SLOPE_MAPS:
            fileName = "maps/slope/" + self.name + ".png"
            if self.slopeMap.read(Filename(fileName)):
                logging.info( "read slopemap from " + fileName)
                return

        self.slopeMap = PNMImage(self.terrain.heightMapSize, self.terrain.heightMapSize)
        self.slopeMap.makeGrayscale()
        self.slopeMap.setMaxval(65535)

        size = self.slopeMap.getYSize()
        getNormal = self.getNormal
        setGray = self.slopeMap.setGray

        for x in range(size):
            for y in range(size):
                #note getNormal works at the same resolution as the heightmap
                normal = getNormal(x, y)
                #  feed pixel into image
                # why is it necessary to invert the y axis I wonder?
                #logging.info( normal)
                normal.z /= self.terrain.getSz()
                normal.normalize()
                slope = 1.0 - normal.dot(Vec3(0, 0, 1))
                setGray(x, y, slope)

        if SAVED_SLOPE_MAPS:
            fileName = "maps/slope/" + self.name + ".png"
            logging.info( "saving slopemap to " + fileName)
            self.slopeMap.write(Filename(fileName))


    def createGroups(self):
        self.statics = self.getRoot().attachNewNode(self.name + "_statics")
        self.statics.setSz(1.0 / self.terrain.getSz())
        self.statics.setSx(1.0 / self.terrain.getSx())
        self.statics.setSy(1.0 / self.terrain.getSy())

        self.statics.setShaderAuto()

    def make(self):
        """Build a finished renderable heightMap."""

        # apply shader
        #logging.info( "applying shader")
        
        if sys.platform == "emscripten":
            print("Not setting tex code because of issues with WEBGL")
        else:
            self.terrain.texturer.apply(self.getRoot())

        # detail settings
        #self.getRoot().setSx(1.0 / self.heightMapDetail)
        #self.getRoot().setSy(1.0 / self.heightMapDetail)

        #logging.info( "making height map")
        self.makeHeightMap()
        #logging.info( "setHeight()")
        self.setHeight()
        #self.getRoot().setSz(self.maxHeight)

        #http://www.panda3d.org/forums/viewtopic.php?t=12054
        if sys.platform == "emscripten":
            print("Not setting ao code because of issues with WEBGL")
        else:
            self.calcAmbientOcclusion()
        #logging.info( "generate()")
        self.generate()
        self.getRoot().setCollideMask(BitMask32.bit(1)) 

        #self.makeSlopeMap()
        #logging.info( "createGroups()")
        self.createGroups()
        self.terrain.populator.populate(self)


###############################################################################
#   LodTerrainTile
###############################################################################

class LodTerrainTile(TerrainTile):
    """Always builds full detail heightmap, but uses panda3d's default LOD
    functions, and hides seams between tiles."""

    def __init__(self, terrain, x, y):
        """Builds a Tile for the terrain at input coordinates."""

        TerrainTile.__init__(self, terrain, x, y)
        self.detail = 2
        self.setMinLevel(2)

    def make(self):
        TerrainTile.make(self)

    def getDetail(self):
        return self.detail

    def setDetail(self, detail):
        if self.detail == detail:
            return
        self.detail = detail
        self.setMinLevel(detail)
        #self.update(None)
        self.generate()
        self.statics.reparentTo(self.getRoot())
        #self.getRoot().setPos(self.xOffset, self.yOffset, 0)


###############################################################################
#   LodTerrainTile2 !! UNUSED !!
###############################################################################

class LodTerrainTile2(NodePath):
    """Loads all detail levels at once but leaves obvious seams."""

    def __init__(self, terrain, x, y):
        """Builds a Tile for the terrain at input coordinates."""

        NodePath.__init__(self, terrain.name)
        self.setMinDetail(2)
        self.make()

    def setDetail(self, detail):
        """This will switch to the necessary detail level.

        If the necessary detail level does not yet exist, it will add it to the
        build Queue on terrain.
        """
        if self.detail == detail:
            return
        self.detail = detail
        if detail in self.detailLevels:
            self._setDetail(detail)
        else:
            self.terrain.buildQueue.append((self, detail))

    def _setDetail(self, detail):
        """This is used internally to swap the correct detail level in."""
        for d, tile in self.detailLevels.iteritems():
            if not d == detail:
                #PandaNode.stashChild(self, tile)
                tile.getRoot().stash()
            else:
                #PandaNode.unstashChild(self, tile)
                tile.getRoot().unstash()

    def buildAndSet(self, detail):
        self.detailLevels[detail] = self.build(detail)
        self._setDetail(detail)


###############################################################################
#   TextureMappedTerrainTile
###############################################################################

class TextureMappedTerrainTile(LodTerrainTile):
    """This terrain tile stores a pnm image map of textures to use."""

    def __init__(self, terrain, x, y):

        LodTerrainTile.__init__(self, terrain, x, y)

        # this sort of thing should really be done in c++
        self.textureMaps = deque()
        self.fourChannel = True

    def make(self):
        TerrainTile.make(self)
        self.makeSlopeMap()
        textureMapper = self.terrain.texturer.textureMapper
        if sys.platform == "emscripten":
            print("Not setting tex code because of issues with WEBGL")
        else:
            #try to read textureMaps
            readTexMaps = True
            texNum = 0
            for tex in textureMapper.textures:
                texNum += 1
                fileName = "maps/textures/" + self.name + "+_texture" + str(texNum) + ".png"
                if not tex.image.read(Filename(fileName)):
                    readTexMaps = False

            #otherwise calculate textureMaps
            if not readTexMaps:
                self.terrain.texturer.textureMapper.calculateTextures(self)

            #copy textureMaps to this terrainTile and save if necessary
            texNum = 0
            for tex in self.terrain.texturer.textureMapper.textures:
                texNum += 1
                self.textureMaps.append(tex.image)
                if not readTexMaps:
                    tex.image.write(Filename("maps/textures/" + self.name + "+_texture" + str(texNum) + ".png"))

            #load textureMaps as actual textures for the shaders use
            num = 0
            for tex in self.textureMaps:
                num += 1
                newTexture = Texture()
                newTexture.load(tex)
                ts = TextureStage('alp' + str(num))
                self.getRoot().setTexture(ts, newTexture)
            #logging.info( self.getRoot().findAllTextureStages())

###############################################################################
#  makeTile
###############################################################################
def makeTile(threadName, terrain, pos):
    tile = pos
    logging.info( threadName+ " is instancing the tile at"+ str(pos))
    if SAVED_TEXTURE_MAPS:
        tile = TextureMappedTerrainTile(terrain, pos[0], pos[1])
    else:
        tile = LodTerrainTile(terrain, pos[0], pos[1])
    logging.info( threadName+ " is building the tile at"+ str(pos))
    tile.make()
#                self.terrain.populator.populate(tile)
    logging.info( threadName+ " finished the tile at"+ str(pos))
    return tile

    
###############################################################################
#  PermanentTileBuilderThread
###############################################################################
class PermanentTileBuilderThread(threading.Thread):
    def __init__(self, queue, out_queue, terrain):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
        self.terrain = terrain

    def run(self):
        # Have our thread serve "forever":
        while True:
            pos = self.queue.get()
            if pos:
                tile = makeTile(self.getName(), self.terrain, pos)
                self.out_queue.put(tile)
                self.queue.task_done()

###############################################################################
#  TransientTileBuilderThread
###############################################################################
class TransientTileBuilderThread(threading.Thread):
    def __init__(self, pos, out_queue, terrain):
        threading.Thread.__init__(self)
        self.pos = pos
        self.out_queue = out_queue
        self.terrain = terrain

    def run(self):
            tile = makeTile(self.getName(), self.terrain, self.pos)
            self.out_queue.put(tile)
          
###############################################################################
#  TerrainTileBuilder
###############################################################################

class TerrainTileBuilder():

    def __init__(self, terrain):
        self.queue = Queue.Queue()
        self.out_queue = Queue.Queue()
        self.terrain = terrain
        self.numTransients = 0

        #spawn a pool of threads, and pass them queue instance
        logging.info( "Loading tile builder threads.")
#        for i in range(1):
#            #try:
#            t = PermanentTileBuilderThread(self.queue, self.out_queue, terrain)
#            t.setName("TileBuilderThread"+str(i))
#            logging.info( "Created "+ t.getName())
#            t.setDaemon(True)
#            t.start()
#            #except:
#            #logging.info( "Unable to start TileBuilderThread!")

        taskMgr.setupTaskChain('tileBuilder', numThreads = 1, tickClock = False,
                           threadPriority = None, frameBudget = -1,
                           frameSync = False, timeslicePriority = True)

        taskMgr.add(self.makeTileTask, 'tileBuilderTask', taskChain = 'tileBuilder')

    def clearQueue(self):
        return
        while self.queue.qsize() > 2:
            try:
                pos = self.queue.get_nowait()
                if pos in self.terrain.tiles:
                    del self.terrain.tiles[pos]
            except:
                logging.info( "Unable to remove old tile from TileBuilder Queue")

    def preload(self, pos):
        #self.queue.put(pos)
        self.build(pos)

    def build(self, pos):
        #self.clearQueue()
        self.queue.put(pos)
        #self.spawnTransientThread(pos)


    def grab(self):
        try:
            return self.out_queue.get_nowait()
        except:
            return None

    def spawnTransientThread(self,pos):
        self.numTransients += 1
        t = TransientTileBuilderThread(pos, self.out_queue, self.terrain)
        t.setName("TileBuilderThread"+str(self.numTransients))
        logging.info( "Created "+ t.getName())
        t.setDaemon(True)
        t.start()

    def makeTileTask(self, task):
        pos = self.queue.get()
        if pos:
            tile = makeTile("tileBuilderTaskChain", self.terrain, pos)
            self.out_queue.put(tile)
        return Task.cont