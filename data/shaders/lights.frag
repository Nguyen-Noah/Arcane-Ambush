#version 330 core

uniform sampler2D light_surf;

in vec2 uv;
out vec4 f_color;

void main() {
    vec3 light_sample = texture(light_surf, uv).rgb;

    float threshold = 0.1;

    if (light_sample.r < threshold) {
        f_color = vec4(light_sample, 1.0);
    } else {
        discard;
    }
}