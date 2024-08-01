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
main.py: This file is the starting point for a demo of the Panda3d Procedural
Terrain Engine.

Additional code from:
The panda3d roaming ralph demo, Gsk, Merlinson

This is my Panda 3d Terrain Engine.
My aim is to create the best possible 100% procedurally generated terrain
"""
from panda3d.core import loadPrcFileData

loadPrcFileData('', 'max-terrain-height 120')
loadPrcFileData('', 'default-fov 60')
loadPrcFileData('', 'default-far 10000')
loadPrcFileData('', 'default-near 0.01')
loadPrcFileData('', 'allow-portal-cull 1')
loadPrcFileData('', 'sync-video #t')
loadPrcFileData('', 'terrain-horizontal-stretch 1.0')
loadPrcFileData('', 'save-height-maps #f')
loadPrcFileData('', 'save-slope-maps #f')
loadPrcFileData('', 'save-texture-maps #f')
loadPrcFileData('', 'save-vegetation-maps #f')
loadPrcFileData('', 'thread-load-terrain #f')
loadPrcFileData('', 'brute-force-tiles #t')
#loadPrcFileData('', 'multisamples 1')
loadPrcFileData('', 'textures-power-2 up')
loadPrcFileData('', 'textures-auto-power-2 #t')

#loadPrcFileData('', 'threading-model Cull/Draw')

import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import *
from direct.particles.Particles import *
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from sky import *
from splashCard import *
from direct.gui.DirectGui import *
from terrain import *
from physics import *
from basicfunctions import *
from camera import *
from config import *
from creature import *
class World(DirectObject):
    def __init__(self):
        print("hi")
        self.temporarygui = NodePath('temporary')
        self.temporarygui.reparentTo(aspect2d)
        self.playing = 1
        self.score = 0
        base.setBackgroundColor(0, 0, 0)
        self.mainFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0),parent=self.temporarygui)
        self.background = OnscreenImage(image = "textures/bg.jpg", pos = (0, 0, 0), scale = (1.5, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.mainFrame)
        self.title = OnscreenText(text="Infinite Sled World",pos=(0,0.8), scale=0.2,fg=(1, 1, 1, 1),parent=self.temporarygui)
        self.startButton = DirectButton(image = "textures/play.png", scale=(0.5,0.5,0.15), relief = None, command=self.loadGame, pos=(0, 0, -0.8),parent=self.temporarygui)
        self.startButton.setTransparency(TransparencyAttrib.MAlpha)
        self.creditsButton = DirectButton(image = "textures/credits.png", scale=(0.3,0.3,0.08),relief = None,  command=self._loadDisplay, pos=(-1, 0, -0.85),parent=self.temporarygui)
        self.creditsButton.setTransparency(TransparencyAttrib.MAlpha)
        self.gameInstructions1 = DirectLabel(text="It's an infinite sledding game!", text_scale=(0.1, 0.1), relief=None, text_fg=(255, 255, 255, 100), pos=(0, 0, 0.5),parent=self.temporarygui)
        self.gameInstructions2 = DirectLabel(text="The goal is simple!", text_scale=(0.1, 0.1), relief=None, text_fg=(255, 255, 255, 100), pos=(0, 0, 0.3),parent=self.temporarygui)
        self.gameInstructions3 = DirectLabel(text="Avoid obstacles!", text_scale=(0.1, 0.1), relief=None, text_fg=(255, 255, 255, 100), pos=(0, 0, 0.1),parent=self.temporarygui)
        self.gameInstructions4 = DirectLabel(text="Sled far!", text_scale=(0.1, 0.1), relief=None, text_fg=(255, 255, 255, 100), pos=(0, 0, -0.1),parent=self.temporarygui)
        self.gameInstructions5 = DirectLabel(text="Use arrow keys to move! Or A and D keys!", text_scale=(0.1, 0.1), relief=None, text_fg=(255, 255, 255, 100), pos=(0, 0, -0.3),parent=self.temporarygui)

     #   self.mySound = loader.loadSfx("music/happy-loop.ogg")
      #  self.mySound.setLoop(True)
       # self.mySound.setLoopCount(0)
        #self.mySound.play()
    def loadGame(self):
        # set here your favourite background color - this will be used to fade to
        for node in self.temporarygui.getChildren():
            node.removeNode()
        bgcolor = (0.2, 0.2, 0.2, 1)
        base.setBackgroundColor(*bgcolor)
        self.splash = SplashCard('textures/loading.png', bgcolor)
        taskMgr.doMethodLater(0.01, self.load, "Load Task")
        self.bug_text = addText(-0.95, "Loading...", True, scale=0.1)


    def load(self, task):
        self.playing = 1
        self.score = 0
        PStatClient.connect()

        self.bug_text.setText("loading Display...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadDisplay()
        
        self.bug_text.setText("loading physics...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadPhysics()
        
        self.bug_text.setText("loading sky...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadSky()

        # Definitely need to make sure this loads before terrain
        self.bug_text.setText("loading terrain...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadTerrain()
        yield Task.cont
        yield Task.cont
        while taskMgr.hasTaskNamed("preloadTask"):
            #logging.info( "waiting")
            yield Task.cont
        logging.info( "terrain preloaded")

        #self.bug_text.setText("loading fog...")
        #showFrame()
        #self._loadFog()

        self.bug_text.setText("loading player...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadPlayer()

        self.bug_text.setText("loading filters...")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self._loadFilters()

        self.bug_text.setText("loading miscellanious...")
        #showFrame()
        yield Task.cont
        yield Task.cont

        self.physics.setup(self.terrain, self.penguin)

        taskMgr.add(self.move, "moveTask")

        # Game state variables
        self.prevtime = 0
        self.isMoving = False
        self.firstmove = 1

        disableMouse()
        self.bug_text.setText("")
        #showFrame()
        yield Task.cont
        yield Task.cont
        self.splash.destroy()
        self.splash = None
        
        yield Task.done
        

    def _loadDisplay(self):
        base.setFrameRateMeter(True)
        self.loc_text = addText(0.95, "Score: ", True)

    def _loadTerrain(self):
        populator = TerrainPopulator()
        populator.addObject(makeTree, {}, 5)
        if SAVED_HEIGHT_MAPS:
            seed = 666
        else:
            seed = 0
        self.terrain = Terrain('Terrain', base.cam, MAX_VIEW_RANGE, populator, feedBackString=self.bug_text, id=seed)
        self.terrain.reparentTo(render)
       # self.terrain.setZ(10)



    def _loadFilters(self):
        # load default shaders
        cf = CommonFilters(base.win, base.cam)
        #bloomSize
        cf.setBloom(size='small', desat=0.7, intensity=0.5, mintrigger=0.6, maxtrigger=0.95)
        #hdrtype:
       # render.setAttrib(LightRampAttrib.makeHdr1())
        #perpixel:
        #render.setShaderAuto()
        #base.bufferViewer.toggleEnable()
    def _loadSky(self):
        self.sky = Sky(None)
        self.sky.start()
    def _loadPlayer(self):
        # Create the main character, penguin
        self.penguin = Player(self.terrain.getElevation, 0, 0)

        self.focus = self.penguin
        self.terrain.setFocus(self.focus)
        # Accept the control keys for movement
                
        self.camera = FollowCamera(self.penguin, self.terrain)
        
        self.mouseInvertY = False
        self.accept("escape", sys.exit)
        # movement controls
        self.accept("a", self.penguin.setControl, ["left", 1])
        self.accept("arrow_left", self.penguin.setControl, ["left", 1])
        self.accept("d", self.penguin.setControl, ["right", 1])
        self.accept("arrow_right", self.penguin.setControl, ["right", 1])
        self.accept("a-up", self.penguin.setControl, ["left", 0])
        self.accept("arrow_left-up", self.penguin.setControl, ["left", 0])
        self.accept("d-up", self.penguin.setControl, ["right", 0])
        self.accept("arrow_right-up", self.penguin.setControl, ["right", 0])
        # other controls
  #      self.accept("shift", self.penguin.setControl, ["turbo", 1])
        self.accept("shift", screenShot)
     #   self.accept("r", self.terrain.initializeHeightMap)
      #  self.accept("l", self.terrain.toggleWireFrame)
       # self.accept("t", self.physics.test) #self.terrain.test)
        #self.accept("e", self.toggleEditor)
     #   self.accept("w-up", self.penguin.setControl, ["forward", 0])

        
   #     self.accept("shift-up", self.penguin.setControl, ["turbo", 0])
        self.accept("wheel_up", self.camera.zoom, [1])
        self.accept("wheel_down", self.camera.zoom, [0])
       # self.accept("tab", self.toggleMenu)
       # continuious forward movement
        self.penguin.setControl("forward",1)
        # snow VFX
        base.enableParticles()
        self.p = ParticleEffect()
        self.p.loadConfig("snow.ptf")
        self.p.setZ(20)
        self.p.setScale(0.5)
        self.p.setY(-100)
        self.p.start(parent = self.penguin, renderParent = render)
        self.p2 = ParticleEffect()
        self.p2.loadConfig("snow.ptf")
        self.p2.setZ(20)
        self.p2.setScale(0.5)
        self.p2.setY(-100)
        self.p2.start(parent = self.penguin, renderParent = render)
        self.p4 = ParticleEffect()
        self.p4.loadConfig("snow.ptf")
        self.p4.setZ(20)
        self.p4.setScale(0.5)
        self.p4.setY(-100)
        self.p4.start(parent = self.penguin, renderParent = render)
        # collision handling for tree coll
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        # player collision
        collider_node = CollisionNode("box-coll")  # collision node for the Player
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 4))  # collision geometry for the Player
        collider_node.setFromCollideMask(BitMask32.bit(0))
        collider_node.addSolid(coll_box)
        collider = self.penguin.attachNewNode(collider_node)
        self.cTrav.addCollider(collider, self.queue)
       # collider.show() # shows the debug box
    def _loadPhysics(self):
        self.physics = TerrainPhysics()
    def toggleMenu(self):
        ml = toggleMouseLook()
        try: self.shaderControl
        except: logging.info( "No shader control found.")
        else: self.shaderControl.setHidden(ml)
    def toggleEditor(self):
        ml = toggleMouseLook()
        self.editor.toggle(not ml)
    def playAgain(self):
        for node in self.temporarygui.getChildren():
            node.removeNode()
        self.penguin.setPos(0,0,100)
        self.playing = 1
        self.penguin.setControl("forward",1)
        
    def stopPenguin(self,task):
        self.playing = 0
        OnscreenText(text="Game Over",pos=(0,0), scale=0.3,fg=(1, 1, 1, 1), parent=self.temporarygui) 
        DirectButton(image = "textures/playagain.png", scale=(0.5,0.5,0.15), relief = None, command=self.playAgain, pos=(0, 0, -0.8), parent=self.temporarygui)
        aspect2d.setTransparency(TransparencyAttrib.MAlpha)

    def move(self, task):
        elapsed = task.time - self.prevtime
        self.camera.update(0, 0)   
        if (self.playing == 1):
            self.penguin.update(elapsed)
        self.score = int(self.penguin.getY() * -1)
        self.loc_text.setText('Score: ' + str(self.score))
        # Store the task time and continue.
        self.prevtime = task.time
        self.cTrav.traverse(render)
        
        for entry in self.queue.getEntries():
            self.penguin.setControl("forward",0)
            myTask = taskMgr.doMethodLater(5, self.stopPenguin, 'tickTask')
       #     print(entry)

        return Task.cont

def launchTerrainDemo():
    logging.info('instancing world...')
    w = World()
    logging.info('calling run()...')
    run()
launchTerrainDemo()
