#version 330 core

in vec2 vert;           // position
in vec2 texcoord;
out vec2 blurTextureCoords[11];

void main() {
    uv = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);

    vec2 centerTexCoords = vert * 0.5 + 0.5;
    float pixelSize = 1 / 720;

    for (int i = -5; i <= 5; i++) {
        blurTextureCoords[i + 5] = centerTexCoords + vec2(0.0, pixelSize * i);
    }
}