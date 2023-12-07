#version 330 core

uniform sampler2D ui;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec4 ui_sample = texture(ui, uvs);
    f_color = ui_sample;
}