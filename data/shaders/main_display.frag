#version 330 core

const int num_lights =  20;

uniform sampler2D surface;
uniform sampler2D noise;
uniform float world_timer;
uniform ivec2 window_dimensions;
uniform ivec2 pixel_dimensions;
uniform ivec2 scroll;
uniform vec2 lights[11];
uniform vec3 color_mix;

const vec3 midnight = vec3(0.03921569, 0.2745098, 0.78431373);
const vec3 late_night = vec3(0.03921569, 0.31372549, 0.8627451);
const vec3 dawn = vec3(0.8627451, 0.78431373, 0.68627451);
const vec3 morning = vec3(0.98039216, 0.92156863, 0.78431373);
const vec3 noon = vec3(1.0, 0.98039216, 0.90196078);
const vec3 late_afternoon = vec3(0.98039216, 0.94117647, 0.78431373);
const vec3 dusk = vec3(0.84313725, 0.58823529, 0.64705882);
const vec3 early_night = vec3(0.03921569, 0.31372549, 0.8627451);

const int number_of_key_times = 8;

in vec2 uv;
out vec4 f_color;

float customSmoothStep(float edge0, float edge1, float x) {
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

void main() {
    vec3 display_sample = texture(surface, uv).rgb;
    
    /* float cloud_timer = world_timer * 0.3;
    vec2 noise_pos1 = vec2(sample_pos_parallax.x * noise_scale * 0.5 - world_timer * 0.02, sample_pos_parallax.y * noise_scale + cos(world_timer * 0.07) * 0.1);
    vec2 noise_pos2 = vec2(sample_pos.x * noise_scale + sin(world_timer * 0.05) * 0.1, sample_pos.y * noise_scale * 3 + cos(world_timer * 0.05) * 0.1);
    vec2 noise_pos3 = vec2(sample_pos_parallax.x * noise_scale * 0.3 - world_timer * 0.035, sample_pos_parallax.y * noise_scale * 0.8 + cos(world_timer * 0.09 + 0.3) * 0.1);
    float noise_val = texture(noise, noise_pos3).r * 0.7 + texture(noise, noise_pos1).r * 0.2 + texture(noise, noise_pos2).r * 0.1;
    float noise_level = min(1, max(0, noise_val - 0.5) * 4);

    display_sample = display_sample * (1.0 - noise_level) + noise_level;
    display_sample = mix(display_sample, vec3(0.0), noise_level); */

    // DAY NIGHT CYCLE -------------------------------------------- //
    vec3 render_color = display_sample * color_mix;

    /* vec3 col = vec3(0.0);
    for (int i = 0; i < lights.length; i++) {
        vec2 light = lights[i];
        float dist = length(uv - light);
        col += 0.1 / dist;
    } 

    render_color = render_color * col; */

   f_color = vec4(render_color, 1.0);
}