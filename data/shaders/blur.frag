#version 330 core

uniform sampler2D surface;

const float weight[6] = float[](0.198596, 0.175713, 0.121703, 0.065984, 0.028002, 0.0093);

in vec2 blurTextureCoords[11];
out vec4 f_color;

void main() {
    f_color = vec4(0.0);
    f_color += texture(surface, blurTextureCoords[0]) * weight[5];
    f_color += texture(surface, blurTextureCoords[1]) * weight[4];
    f_color += texture(surface, blurTextureCoords[2]) * weight[3];
    f_color += texture(surface, blurTextureCoords[3]) * weight[2];
    f_color += texture(surface, blurTextureCoords[4]) * weight[1];
    f_color += texture(surface, blurTextureCoords[5]) * weight[0];
    f_color += texture(surface, blurTextureCoords[6]) * weight[1];
    f_color += texture(surface, blurTextureCoords[7]) * weight[2];
    f_color += texture(surface, blurTextureCoords[8]) * weight[3];
    f_color += texture(surface, blurTextureCoords[9]) * weight[4];
    f_color += texture(surface, blurTextureCoords[10]) * weight[5];
}