#version 330 core

uniform sampler2D surface;
uniform sampler2D perlin_noise;
uniform float world_timer;
uniform vec2 base_resolution;
uniform float i_frames;

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, vec2(uv.x, uv.y));
    
    float aspect_ratio = base_resolution.x / base_resolution.y;

    // Adjusted uv to render circles as circles instead of ovals
    float aspect_shift = (aspect_ratio - 1) * 0.5;
    vec2 adjusted_uv = vec2(uv.x * aspect_ratio - aspect_shift, uv.y);

    vec2 pixel_uv = vec2(floor(uv.x * base_resolution.x) / base_resolution.x, floor(uv.y * base_resolution.y) / base_resolution.y);
    vec4 perlin_noise = texture(perlin_noise, vec2(pixel_uv.x * aspect_ratio * 2 + (world_timer * 0.1), pixel_uv.y * 2 - (world_timer * 0.1)));

    vec3 render_color = vec3(0.0);

    render_color = display_sample.rgb;

    // Noise edge
    float center_dist = distance(uv, vec2(0.5));
    float noise_val = center_dist + perlin_noise.r * 0.55;
    vec3 dark_color = vec3(0.0, 0.0, 0.0);
    if (noise_val > 0.95) {
        render_color = vec3(0.011764705882352941, 0.043137254901960784, 0.08627450980392157);
    } else if (noise_val > 0.9) {
        render_color = vec3(0.0, 0.06274509803921569, 0.12549019607843137);
    } else {
        float darkness = max(0, noise_val - 0.75) * 2.5;
        render_color = darkness * dark_color + (1 - darkness) * render_color;
    }


    // DAMAGE VIGNETTE -------------------------------------------- //
    
    // Red color for the vignette
    vec3 redColor = vec3(0.3, 0.0, 0.0);
    float greyness = max((center_dist - 0.2) * (i_frames * 3), 0);
    // Applying the red vignette
    render_color = mix(render_color, redColor, greyness * 0.9);

    f_color = vec4(render_color, 1.0);
}