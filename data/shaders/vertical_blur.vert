#version 330 core

in vec2 vert;           // position
in vec2 texcoord;
out vec2 blurTextureCoords[17];

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);

    vec2 centerTexCoords = vert * 0.5 + 0.5;
    float pixelSize = 1.0 / 1080;

    for (int i = -8; i <= 8; i++) {
        blurTextureCoords[i+8] = centerTexCoords + vec2(0.0, pixelSize * i);
    }
}