#version 330 core

uniform sampler2D surface;
uniform sampler2D light_surf;
uniform float ratio;

in vec2 uv;
out vec4 f_color;

void main() {
    vec3 display_sample = texture(surface, uv).rgb;
    vec4 light_sample = texture(light_surf, uv);

    vec3 render_color = vec3(0.0);
    light_sample.a = 0.6;
    render_color = display_sample + light_sample.rgb;

    f_color = light_sample;
}