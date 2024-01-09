#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uv;

void main() {
    uv = vec2(texcoord.x, 1.0-texcoord.y);
    gl_Position = vec4(vert, 0.0, 1.0);
}