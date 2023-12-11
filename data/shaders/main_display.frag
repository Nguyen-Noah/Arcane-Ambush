#version 330 core

const int num_lights =  20;

uniform sampler2D surface;
uniform sampler2D noise;
uniform float world_timer;
uniform vec2 lights[11];
uniform vec3 color_mix;

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
    float grey = dot(display_sample, vec3(0.299, 0.587, 0.114));
    vec3 render_color = grey > 0.5 ? 1.0 - (1.0 - 2.0 * (display_sample - 0.5)) * (1.0 - color_mix) : 2.0 * display_sample * color_mix;

    render_color = display_sample * color_mix;

    vec3 col = vec3(0.0);
    for (int i = 0; i < lights.length; i++) {
        vec2 light = lights[i];
        float dist = length(uv - light);
        col += 0.01 / dist;
    }

    render_color = render_color * col;

   f_color = vec4(render_color, 1.0);
}