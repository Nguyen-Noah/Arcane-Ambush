import moderngl, pygame
from array import array
from .core_funcs import read_f
from .config import config

class MGL:
    def __init__(self):
        self.ctx = moderngl.create_context()
        self.textures = {}
        self.programs = {}
        self.fbos = {}
        self.fbo_textures = {}
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
        self.load_texture('perlin_noise')
        self.compile_program('screen', 'screen', 'main_display')
        self.compile_program('texture', 'main_display', 'game_display')
        self.compile_program('texture', 'ui', 'ui')
        # post processing
        self.compile_program('texture', 'bright_filter', 'luma_filter')
        self.create_framebuffer('test')
        self.create_framebuffer('luma_filter')

    def load_texture(self, name):
        surf = pygame.image.load('data/graphics/misc/' + name + '.png').convert()
        self.pg2tx(surf, name)

    def compile_program(self, vert_src, frag_src, program_name):
        vert_raw = read_f('./data/shaders/' + vert_src + '.vert')
        frag_raw = read_f('./data/shaders/' + frag_src + '.frag')
        program = self.ctx.program(vertex_shader=vert_raw, fragment_shader=frag_raw)
        self.programs[program_name] = program
        # render object
        self.vaos[program_name] = self.ctx.vertex_array(program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def render(self, world_timer, base_resolution, lights_pos, light_rad_int, light_colors, i_frames):
        # ------------------------------------------------- RENDERING PIPELINE ------------------------------------------------- #

        # clear everything so your gpu doesnt explode
        self.ctx.clear()
        self.clear_fbos()

        self.fbos['luma_filter'].use()
        self.ctx.enable(moderngl.BLEND)
        if 'base_display' in self.textures:
            self.update('luma_filter', {
                'surface': self.textures['base_display']
            })

        # use the test fbo
        self.fbos['test'].use()
        if 'base_display' in self.textures:
            self.update_render('game_display', {
                'surface': self.textures['base_display'],
                'perlin_noise': self.textures['perlin_noise'],
                'world_timer': world_timer,
                'base_resolution': base_resolution,
                'lights': lights_pos,
                'light_rad_int': light_rad_int,
                'light_colors': light_colors,
                'i_frames': i_frames
            })

        # switch to the main screen fbo
        self.ctx.screen.use()
        if 'luma_filter' in self.fbo_textures:
            self.update_render('main_display', {
                'surface': self.fbo_textures['luma_filter']
            })
        if 'ui_surf' in self.textures:
            self.update_render('ui', {
                'surface': self.textures['ui_surf']
            })
        self.ctx.disable(moderngl.BLEND)
        pygame.display.flip()

    def update(self, program_name, uniforms):
        self.update_shader(program_name, uniforms)

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

    def clear_fbos(self):
        for fbo in self.fbos:
            self.fbos[fbo].clear()

    def create_framebuffer(self, fbo_name):
        channels = 4
        if fbo_name not in self.fbo_textures:
            new_fbo = self.ctx.texture(config['window']['base_resolution'], channels)
            new_fbo.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.fbo_textures[fbo_name] = new_fbo
            self.fbos[fbo_name] = self.ctx.framebuffer(color_attachments=[new_fbo])

    def pg2tx(self, surf, texture_name):
        channels = 4
        if texture_name not in self.textures:
            new_tex = self.ctx.texture(surf.get_size(), channels)
            new_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
            new_tex.swizzle = 'BGRA'
            self.textures[texture_name] = new_tex

        texture_data = surf.get_view('1')
        self.textures[texture_name].write(texture_data)