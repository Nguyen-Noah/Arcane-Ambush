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
        self.compile_program('horizontal_blur', 'blur', 'horizontal_blur')
        self.compile_program('vertical_blur', 'blur', 'vertical_blur')
        self.compile_program('texture', 'bloom', 'combine_bloom')

        self.create_framebuffer('overlays')
        self.create_framebuffer('luma_filter')
        self.create_framebuffer('horizontal_blur', filter=(moderngl.LINEAR, moderngl.LINEAR))
        self.create_framebuffer('vertical_blur', filter=(moderngl.LINEAR, moderngl.LINEAR))
        self.create_framebuffer('combine_bloom')

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

    def render(self, world_timer, base_resolution, i_frames):
        # ------------------------------------------------- RENDERING PIPELINE ------------------------------------------------- #

        # clear everything so your gpu doesnt explode
        self.ctx.clear()
        self.clear_fbos()
        self.ctx.enable(moderngl.BLEND)    

        """
        self.fbos['luma_filter'].use()
        if 'base_display' in self.textures:
            self.update_render('luma_filter', {
                'surface': self.textures['base_display']
            })

        self.fbos['horizontal_blur'].use()
        self.update_render('horizontal_blur', {
            'surface': self.fbos['luma_filter'].color_attachments[0]
        })

        self.fbos['vertical_blur'].use()
        self.update_render('vertical_blur', {
            'surface': self.fbos['horizontal_blur'].color_attachments[0]
        })

        self.fbos['combine_bloom'].use()
        self.update_render('combine_bloom', {
            'surface': self.textures['base_display'],
            'blurred_surface': self.fbos['vertical_blur'].color_attachments[0]
        }) """

        self.fbos['overlays'].use()
        if 'base_display' in self.textures:
            self.update_render('game_display', {
                'surface': self.textures['base_display'],
                'perlin_noise': self.textures['perlin_noise'],
                'world_timer': world_timer,
                'base_resolution': base_resolution,
                'i_frames': i_frames
            })

        # switch to the main screen fbo
        self.ctx.screen.use()
        if 'overlays' in self.fbos:
            self.update_render('main_display', {
                'surface': self.fbos['overlays'].color_attachments[0]
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

    def clear_fbos(self):
        for fbo in self.fbos:
            self.fbos[fbo].clear()

    def create_framebuffer(self, fbo_name, display_resize=1, filter=(moderngl.NEAREST, moderngl.NEAREST)):
        channels = 4
        if fbo_name not in self.fbos:
            new_fbo = self.ctx.texture((config['window']['scaled_resolution'][0] // display_resize, config['window']['scaled_resolution'][1] // display_resize), channels)
            new_fbo.filter = filter
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