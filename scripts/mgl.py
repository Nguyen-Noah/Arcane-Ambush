import moderngl
from array import array
from .core_funcs import read_f

class MGL:
    def __init__(self, game):
        self.game = game
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        vert_shader = read_f('./data/shaders/texture.vert')

        frag_shader = read_f('./data/shaders/texture.frag')

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex