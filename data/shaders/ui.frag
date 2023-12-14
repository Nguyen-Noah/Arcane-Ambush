#version 330 core

uniform sampler2D ui;

const vec2 shadow_shift = vec2(-0.0027, -0.0042);

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 ui_sample = texture(ui, uv);

    // UI SHADOW
    if (ui_sample.a == 0) {
        vec4 ref = texture(ui, uv + shadow_shift);
        if (ref.a != 0) {
            ui_sample = vec4(0.0, 0.0, 0.01, 1.0);
        }
    }
    f_color = ui_sample;
}