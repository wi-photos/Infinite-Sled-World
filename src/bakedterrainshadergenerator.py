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
bakedterrainshadergenerator.py: 
"""

from terrainshadergenerator import *


###############################################################################
#   BakedTerrainShaderGenerator
###############################################################################

class BakedTerrainShaderGenerator(TerrainShaderGenerator):

    def getVertexFragmentConnector(self):
        vfconn = '''
struct vfconn
{
    //from terrain shader
    float2 l_tex_coord : TEXCOORD0;
    float2 l_tex_coord3 : TEXCOORD3;
    float3 l_normal : TEXCOORD1;
    float3 l_world_pos : TEXCOORD2;
    float4 l_color : COLOR;

    //from auto shader
    float4 l_eye_position : TEXCOORD4;
    float4 l_eye_normal : TEXCOORD5;

'''
        if self.fogDensity:
            vfconn += '''
    float l_fog : FOG;'''

        vfconn += '''
};
'''
        return vfconn


    def getFShaderTerrainParameters(self):

        texNum = 0
        string = ''
        #base textures
        for tex in self.textureMapper.textures:
            string += '''
            in uniform sampler2D tex_''' + str(texNum) + ','
            texNum += 1
        texNum = 0
        #alpha maps
        for tex in self.textureMapper.textures:
            string += '''
            in uniform sampler2D map_''' + str(texNum) + ','
            texNum += 1
        string = string[:-1] + '''
) {
'''
        return string #trim last comma


    def getTerrainPrepCode(self):
        fshader = ''
#        if self.fogDensity:
        if False:
            fshader += '''
        if (input.l_fog == 1.0)
        {
            o_color = fogColor;
            return;
        }
'''
        fshader += '''
        //set up texture calculations
        // Fetch all textures.
        float slope = 1.0 - dot( input.l_normal, vec3(0,0,1));
        vec4 terrainColor = float4(0.0, 0.0, 0.0, 1.0);

'''
        return fshader


    def getTerrainTextureCode(self):

        texNum = 0
        string = ''
        for tex in self.textureMapper.textures:
            string += '''
                float4 tex''' + str(texNum) + ' = tex2D(tex_' + str(texNum) + ', input.l_tex_coord);'
            texNum += 1

        texNum = 0
        for tex in self.textureMapper.textures:
            string += '''
                float alpha''' + str(texNum) + ' = tex2D(map_' + str(texNum) + ', input.l_tex_coord3).a;'
            texNum += 1

        texNum = 0
        for tex in self.textureMapper.textures:
            string += '''
                terrainColor += tex''' + str(texNum) + ' * alpha' + str(texNum) + ' * 1.0;'
            #terrainColor = tex2D(tex_2, input.l_tex_coord) * tex2D(tex_4, input.l_tex_coord).a* 5.5;'''
            #terrainColor += tex'''+ str(texNum) +'*1.5;'''

            texNum += 1
        return string


    def saveShader(self, name='shaders/FullTerrain.sha'):
        TerrainShaderGenerator.saveShader(self, name)