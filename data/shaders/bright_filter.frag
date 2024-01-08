#version 330 core

uniform sampler2D surface;

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, uv);

    float brightness = (display_sample.r * 0.2126) + (display_sample.g * 0.7152) + (display_sample.b * 0.0722);
    f_color = display_sample * brightness;
}