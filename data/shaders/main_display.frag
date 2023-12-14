#version 330 core

const int num_lights =  20;

uniform sampler2D surface;
uniform sampler2D noise;
uniform sampler2D light_surf;
uniform float world_timer;
uniform vec2 lights[11];
uniform vec3 color_mix;
uniform float i_frames;

const float light_radius = 0.1;
const vec3 light_color = vec3(1.0, 0.5, 0.5);
const float intensity = 0.8;

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, uv);

    // DAY NIGHT CYCLE -------------------------------------------- //
    float grey = dot(display_sample.rgb, vec3(0.299, 0.587, 0.114));
    vec3 render_color = grey > 0.5 ? 1.0 - (1.0 - 2.0 * (display_sample.rgb - 0.5)) * (1.0 - color_mix) : 2.0 * display_sample.rgb * color_mix;

    render_color = display_sample.rgb * color_mix;

    // VIGNETTE
    float center_dist = distance(uv, vec2(0.5));
    
    // Red color for the vignette
    vec3 redColor = vec3(0.3, 0.0, 0.0);
    
    float greyness = max((center_dist - 0.2) * (i_frames * 3), 0);

    // Applying the red vignette
    vec3 vignette_color = mix(render_color, redColor, greyness * 0.9);

    f_color = vec4(vignette_color, 1.0);
}