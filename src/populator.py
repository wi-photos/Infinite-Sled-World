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
populator.py: This file contains code to populate terrain tiles with objects
"""

from terraintile import *
from direct.showbase.RandomNumGen import *
from panda3d.core import *
from config import *
import random

class LeafModel():
    def __init__(self):
        #print name, nrplates, width, height, shaderfile, texturefile, uvlist, jitter
      #  self.name = name
       # self.texturefile = texturefile
    #    self.shaderfile = shaderfile

        self.np = NodePath('tree')
        t2 = loader.loadModel( 'models/tree.egg' )
        t2.setTwoSided( True )
        t2.reparentTo(self.np)
copy = NodePath()

tree = LeafModel()

def makeTree():
    np = tree.np.copyTo( copy )
    np.setH(random.randint(0, 180))
    np.setScale(random.randint(1, 2))
    cs = CollisionSphere(0, 0, 0, 1)
    cnodePath = np.attachNewNode(CollisionNode('cnode'))
    cnodePath.node().addSolid(cs)
    #cnodePath.show()
    return np

sphere = loader.loadModel("models/sphere")

def makeSphere():
    np = NodePath()
    sphere.copyTo( np )
    logging.info( np)
    return np

class Factory():
    def __init__(self, factoryFunction, constructorParams, averageNumber):
        self.factoryFunction = factoryFunction
        self.constructorParams = constructorParams
        self.averageNumber = averageNumber

class TerrainPopulator():

    def __init__(self):
        self.factories = []

    def addObject(self, factoryFunction, constructorParams, averageNumber):
        factory = Factory(factoryFunction, constructorParams, averageNumber)
        self.factories.append(factory)

    def populate(self, tile):
        terrain = tile.terrain
        xOff = tile.xOffset
        yOff = tile.yOffset
        tileSize = terrain.tileSize

      #  seed = terrain.heightMap.getHeight(yOff * -2, xOff * -2)+1 * 2147483647
        seed = terrain.heightMap.getHeight(yOff, xOff) * 2147483647
        
        dice = RandomNumGen(seed)

        for factory in self.factories:
            #num = dice.randint(0, factory.averageNumber) + dice.randint(0, factory.averageNumber)
            num = int((dice.random() + dice.random()) * factory.averageNumber)
            for iterator in range(num):
                x = dice.random() * tileSize
                y = dice.random() * tileSize
                if terrain.getHeight(x+xOff, y+yOff) > terrain.waterHeight:
                    object = factory.factoryFunction(*factory.constructorParams)
                    #logging.info( object)
                    #logging.info( factory.factoryFunction)
                    self.addToTile(tile, object, x, y)
        tile.statics.flattenStrong()

    def addToTile(self, tile, object, x, y):
        #logging.info("addToTile")
        test = tile.statics
        object.reparentTo(tile.statics)
        #z = tile.terrain.getElevation(x + tile.xOffset, y + tile.yOffset)
        #print z
        z = tile.terrain.getHeight(x + tile.xOffset, y + tile.yOffset)
        #print z
        object.setPos(render, x + tile.xOffset, y + tile.yOffset, z)
        #object.setScale(100.0)
