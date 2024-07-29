"""
This file is adapted from the Panda3D Procedural Terrain Engine project (https://github.com/StephenLujan/Panda-3d-Procedural-Terrain-Engine).
Copyright Stephen Lujan. Used for this project with permission.


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
from pandac.PandaModules import TextNode, CardMaker
from pandac.PandaModules import Vec3,Vec4,Point3,Point2
from pandac.PandaModules import Shader, Texture, TextureStage, TransparencyAttrib
from config import *
import random

class LeafModel():
    def __init__(self, name, nrplates, width, height, shaderfile, texturefile, uvlist, jitter=-1):
        #print name, nrplates, width, height, shaderfile, texturefile, uvlist, jitter
        self.name = name
        self.texturefile = texturefile
        self.shaderfile = shaderfile

        self.np = NodePath('leaf')
        t2 = loader.loadModel( 'models/tree.egg' )
        t2.setTwoSided( True )
        t2.reparentTo(self.np)
        
        '''
        self.tex = loader.loadTexture('textures/' + texturefile)
        self.tex.setMinfilter( Texture.FTLinearMipmapLinear )
        self.tex.setMagfilter( Texture.FTLinearMipmapLinear )
        self.tex.setAnisotropicDegree(2)
        self.np.setTexture( self.tex )
        self.np.setTwoSided( True )
        self.np.setTransparency( TransparencyAttrib.MAlpha )
        #self.np.setTransparency( TransparencyAttrib.MMultisample )
        self.np.setDepthWrite( False )

        maker = CardMaker( 'leaf' )
        maker.setFrame( -width/2.0, width/2.0, 0, height)
        #maker.setFrame( 0,1,0,1)
        for i in range(nrplates):
            if uvlist != None:
                maker.setUvRange(uvlist[i][0],uvlist[i][1])
            else:
                maker.setUvRange(Point2(0,0),Point2(1,0.98))
            node = self.np.attachNewNode(maker.generate())
            #node.setTwoSided( True )
            node.setHpr(i * 180.0 / nrplates,0,0)
        self.np.flattenStrong()
        #np.flattenLight()
        #np.setTwoSided( True )

        if jitter == -1:
            self.jitter = height/width/2
        else:
            self.jitter = jitter
        '''
copy = NodePath()

tree = LeafModel("Tree 1", 3, 5.0, 5.0, None, 'Bleech.png', None)
#tree = NodePath('leaf')
#tree = loader.loadModel( 'models/tree.egg' )
def makeTree():
    np = tree.np.copyTo( copy )
    np.setH(random.randint(0, 180))
    np.setScale(random.randint(1, 2))
    
    #np = self.model.instanceTo( self.grassNP )
    #np = loader.loadModel( 'models/grass.egg' )
    #np.reparentTo(self.grassNP)
    #np.setTwoSided( True )
    #np.setHpr(Vec3(heading,0,0))
    #np.setPos(pos)
    #logging.info( np)
    return np

sphere = loader.loadModel("models/sphere")

def makeSphere():
    np = NodePath()
    sphere.copyTo( np )
    
    #np = self.model.instanceTo( self.grassNP )
    #np = loader.loadModel( 'models/grass.egg' )
    #np.reparentTo(self.grassNP)
    #np.setTwoSided( True )
    #np.setHpr(Vec3(heading,0,0))
    #np.setPos(pos)
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
