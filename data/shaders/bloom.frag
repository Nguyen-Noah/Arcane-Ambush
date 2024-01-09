#version 330 core

uniform sampler2D surface;
uniform sampler2D blurred_surface;

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, uv);
    vec4 blurred_surf = texture(blurred_surface, vec2(uv.x, 1.0-uv.y));
    float intensity = 1.0;

    f_color = display_sample + (blurred_surf * intensity);
}