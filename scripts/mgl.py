import moderngl, pygame
from array import array
from .core_funcs import read_f

class MGL:
    def __init__(self):
        self.ctx = moderngl.create_context()
        self.textures = {}
        self.programs = {}
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))
        self.vaos = {}

        self.initialize()

    def initialize(self):
        self.compile_program('texture', 'default_shader', 'default_texture')
        self.compile_program('texture', 'main_display', 'game_display')
        self.compile_program('texture', 'default_shader', 'ui')

    def compile_program(self, vert_src, frag_src, program_name):
        vert_raw = read_f('./data/shaders/' + vert_src + '.vert')
        frag_raw = read_f('./data/shaders/' + frag_src + '.frag')
        program = self.ctx.program(vertex_shader=vert_raw, fragment_shader=frag_raw)
        self.programs[program_name] = program
        # render object
        self.vaos[program_name] = self.ctx.vertex_array(program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def render(self, world_timer):
        self.ctx.clear()
        self.ctx.enable(moderngl.BLEND)
        if 'base_display' in self.textures:
            self.update_render('game_display', {
                'surface': self.textures['base_display'],
                'world_timer': world_timer,
                'window_dimensions': pygame.display.get_window_size()
            })
        if 'ui_surf' in self.textures:
            self.update_render('ui', {
                'surface': self.textures['ui_surf']
            })
        self.ctx.disable(moderngl.BLEND)
        pygame.display.flip()

    def update_render(self, program_name, uniforms):
        self.update_shader(program_name, uniforms)
        self.vaos[program_name].render(mode=moderngl.TRIANGLE_STRIP)

    def update_shader(self, program_name, uniforms):
        tex_id = 0
        for uniform in uniforms:
            try:
                if type(uniforms[uniform]) == moderngl.Texture:
                    uniforms[uniform].use(tex_id)
                    self.programs[program_name][uniform].value = tex_id
                    tex_id += 1
                else:
                    self.programs[program_name][uniform].value = uniforms[uniform]
            except:
                pass

    def pg2tx(self, surf, texture_name):
        channels = 4
        if texture_name not in self.textures:
            new_tex = self.ctx.texture(surf.get_size(), channels)
            new_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
            new_tex.swizzle = 'BGRA'
            self.textures[texture_name] = new_tex

        texture_data = surf.get_view('1')
        self.textures[texture_name].write(texture_data)