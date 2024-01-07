#version 330 core

in vec2 vert;
in vec2 texcoord;

out vec2 uv;

void main() {
    // flip the uv because for some reason when rendering from fbo it flips it
    uv = vec2(texcoord.x, -texcoord.y);
    gl_Position = vec4(vert, 0.0, 1.0);
}
