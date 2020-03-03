from OpenGL.GL import *
from OpenGL.GL.EXT import texture_compression_s3tc
import struct
import numpy as np

import tools.file_tools as ft


class Texture:
    head = None
    height = None
    width = None
    format = None
    textureGLID = None
    texture_buffer = None
    inversedVCoords = None

    def __init__(self, texture_name, text_type=None):
        self.load_texture(texture_name)

    def load_texture(self, texture_name):
        self.head, self.texture_buffer = ft.load_texture_file(texture_name)
        height, = self.height = struct.unpack("I", self.head[8:12])
        width, = self.width = struct.unpack("I", self.head[12:16])
        mipMapCount, = struct.unpack("I", self.head[24:28])
        fourCC = self.head[80:84]

        self.format = fourCC

        if fourCC == b"DXT1":
            components = 3
            blockSize = 8
        else:
            components = 4
            blockSize = 16

        if fourCC == b"DXT1":
            self.format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT1_EXT
        elif fourCC == b"DXT3":
            self.format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT3_EXT
        elif fourCC == b"DXT5":
            self.format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT5_EXT

        offset = 0
        self.textureGLID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureGLID)

        for level in range(0, mipMapCount):
            size = int(((width + 3) / 4) * ((height + 3) / 4) * blockSize)
            buffer = np.array(self.texture_buffer[offset:offset + size])
            print(buffer.nbytes) # size
            glCompressedTexImage2D(GL_TEXTURE_2D, level, self.format, width, height,
                                   0, buffer.nbytes, buffer)
            offset += size
            width /= 2
            height /= 2
            if width == 0 | height == 0:
                # print "___",width,height,level,mipMapCount
                break
        self.inversedVCoords = True
