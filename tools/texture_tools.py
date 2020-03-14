
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
    Texture_loc = None
    texture_buffer = None
    uvbuffer = None
    inversedVCoords = None

    def init_texture(self, texture_name, texture_type=ft.TEXTURE_PNG):
        if texture_type == ft.TEXTURE_DDS:
            self.init_dds_texture(texture_name, texture_type)
        elif texture_type == ft.TEXTURE_PNG:
            self.init_png_texture(texture_name, texture_type)

    def init_dds_texture(self, texture_name, texture_type):
        self.head, self.texture_buffer = ft.load_texture_file(texture_name, texture_type)
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

            # get which compressed texture GPU support
            # extensions = glGetString(GL_EXTENSIONS)
            # print(extensions)

            buffer = np.array(self.texture_buffer[offset:offset + size])
            print(buffer.nbytes)  # size

            glCompressedTexImage2D(GL_TEXTURE_2D, level, self.format, width, height,
                                   0, buffer.nbytes, self.texture_buffer[offset:offset + size])
            offset += size
            width /= 2
            height /= 2
            if width == 0 | height == 0:
                # print "___",width,height,level,mipMapCount
                break
        self.inversedVCoords = True

    def init_png_texture(self, texture_name, texture_type):
        self.head, self.texture_buffer = ft.load_texture_file(texture_name, texture_type)
        self.height = self.head['height']
        self.width = self.head['width']
        self.format = self.head['mode']

        self.textureGLID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureGLID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_buffer)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)


