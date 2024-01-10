#version 330 core

uniform sampler2D surface;
uniform sampler2D light_surf;
uniform float ratio;

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, uv);
    vec4 light_sample = texture(light_surf, vec2(uv.x, -uv.y));

    vec4 light_col;

    /* light_col.r = light_sample.r * 5.0;
    light_col.g = light_sample.g * 5.0;
    light_col.b = light_sample.b * 5.0;

    f_color.r = mix(display_sample.r, display_sample.r * light_sample.r, light_sample.r);
    f_color.g = mix(display_sample.g, display_sample.g * light_sample.g, light_sample.g);
    f_color.b = mix(display_sample.b, display_sample.b * light_sample.b, light_sample.b);
    f_color.a = 1.0;

    float darkness = 0.4;

    f_color.r = mix(f_color.r, f_color.r * darkness, -light_sample.r);
    f_color.g = mix(f_color.g, f_color.g * darkness, -light_sample.g);
    f_color.b = mix(f_color.b, f_color.b * darkness, -light_sample.b); */
    f_color = light_sample;
}