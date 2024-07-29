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
pstat_debug.py

This pstat function decorator will track a function within the pstat tool.
This is the easiest way to profile slow code for Panda3d.
"""

def pstat(func):
    from pandac.PandaModules import PStatCollector
    collectorName = "Debug:%s" % func.__name__
    if hasattr(base, 'custom_collectors'):
        if collectorName in base.custom_collectors.keys():
            pstat = base.custom_collectors[collectorName]
        else:
            base.custom_collectors[collectorName] = PStatCollector(collectorName)
            pstat = base.custom_collectors[collectorName]
    else:
        base.custom_collectors = {}
        base.custom_collectors[collectorName] = PStatCollector(collectorName)
        pstat = base.custom_collectors[collectorName]
    def doPstat(*args, **kargs):
        pstat.start()
        returned = func(*args, **kargs)
        pstat.stop()
        return returned
    doPstat.__name__ = func.__name__
    doPstat.__dict__ = func.__dict__
    doPstat.__doc__ = func.__doc__
    return doPstat