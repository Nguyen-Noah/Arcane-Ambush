/* #version 330 core

uniform sampler2D surface;

const float weight[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216); 

in vec2 uv;
out vec4 f_color;

void main() {
    vec4 display_sample = texture(surface, uv);
    float brightness = (display_sample.r * 0.2126) + (display_sample.g * 0.7152) + (display_sample.b * 0.722);
    vec3 render_color = display_sample * brightness;

    for (int i = -4; i <= 4; i++) {
        float offset = 1 / 1080;
        render_color += texture(display_sample, uv + offset).rgb * weight[abs(i)];
    }
} */

#version 330 core

uniform sampler2D surface;

const float weight[5] = float[](0.198596, 0.121703, 0.065984, 0.028002, 0.0093)

in vec2 blurTextureCoords[11];
out vec4 f_color;

void main() {
    f_color = vec4(0.0);
    
    for (int i = -5; i <=5; i++) {
        f_color += texture(surface, blurTextureCoords[i + 5]) * weight[(abs)]
    }

}

/* #version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

const float offset = 1.0/640.0;
const float weight[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216); 

// Applies bloom filter to the texture based on sampling neighboring pixels. 
// Uses a weighted average of multiple sample points to approximate a Gaussian blur.
// Checks if the texture is dark and only applies blur to dark areas.

void main()
{
    vec3 color = texture(tex, uvs).rgb;
    
    if (dot(color, vec3(0.2126, 0.7152, 0.0722)) < 0.15) {
        
        vec3 result = color * weight[0];
        
        for(int i = -4; i <= 4; i++) {
            for(int j = -4; j <= 4; j++) {
                vec2 offset = vec2(j, i) * offset; 
                result += texture(tex, uvs + offset).rgb * weight[abs(i)] * weight[abs(j)];
            }
        }
        
        f_color = vec4(result, 1.0);
        
    } else {
        f_color = vec4(color, 1.0); 
    }
} */