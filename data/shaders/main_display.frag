#version 330 core

const int num_lights =  20;

uniform sampler2D surface;
uniform sampler2D noise;
uniform sampler2D light_surf;
uniform float world_timer;
uniform vec2 lights[11];
uniform vec3 color_mix;

const float light_radius = 0.1;
const vec3 light_color = vec3(1.0, 0.5, 0.5);
const float intensity = 0.8;

in vec2 uv;
out vec4 f_color;

void main() {
    vec3 display_sample = texture(surface, uv).rgb;

    // DAY NIGHT CYCLE -------------------------------------------- //
    float grey = dot(display_sample, vec3(0.299, 0.587, 0.114));
    vec3 render_color = grey > 0.5 ? 1.0 - (1.0 - 2.0 * (display_sample - 0.5)) * (1.0 - color_mix) : 2.0 * display_sample * color_mix;

    render_color = display_sample * color_mix;


    f_color = vec4(render_color, 1.0);
}