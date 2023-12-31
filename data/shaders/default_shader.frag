#version 330

uniform sampler2D surface;

out vec4 f_color;
in vec2 uv;

void main() {
    vec4 texColor = texture(surface, uv);

    // Discard pixels with zero alpha
    if (texColor.a == 0.0) {
        discard;
    }

    f_color = texColor;
}
