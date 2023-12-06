#version 330 core

uniform sampler2D tex;
uniform float world_timer;

const vec3 midnight_color = vec3(0.00392169, 0.27450980, 0.78431373);
const vec3 dawn_color = vec3(0.98039216, 0.92156863, 0.78431373);
const vec3 late_afternoon_color = vec3(0.98039216, 0.94117647, 0.78431373);

in vec2 uvs;
out vec4 f_color;

float customSmoothStep(float edge0, float edge1, float x) {
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

void main() {
    vec4 pixel = texture(tex, uvs);

    float wrapped_world_timer = mod(world_timer, 1.0);

    vec3 timeColor;
    if (wrapped_world_timer < 0.25) {
        timeColor = mix(midnight_color, dawn_color, customSmoothStep(0.0, 0.25, wrapped_world_timer));
    } else if (wrapped_world_timer < 0.5) {
        timeColor = mix(dawn_color, late_afternoon_color, customSmoothStep(0.25, 0.5, wrapped_world_timer));
    } else  {
        timeColor = mix(late_afternoon_color, midnight_color, customSmoothStep(0.5, 0.75, wrapped_world_timer));
    }

    f_color = vec4(timeColor * pixel.rgb, 1.0);
}