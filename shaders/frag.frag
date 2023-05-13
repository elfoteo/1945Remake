#version 330 core

uniform sampler2D tex;
uniform float shake_x;
uniform float shake_y;
uniform float red_overlay;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x+shake_x*0.01, uvs.y+shake_y*0.01);
    float i;
    // This code simpy fills the shake zone with black
    if (uvs.x <= 0+shake_x*0.01 || uvs.x >= 1-shake_x*0.01 || uvs.y <= 0+shake_y*0.01 || uvs.y >= 1-shake_y*0.01){
        i = 0;
    }
    else{
        i = 1;
    }
    // Red overlay when damage taken
    vec2 temp_uvs = uvs;
    temp_uvs.x = (abs(temp_uvs.x-0.5));
    temp_uvs.y = (abs(temp_uvs.y-0.5));
    f_color = vec4(texture(tex, sample_pos).r*(i*(1+red_overlay*0.9))+((red_overlay)*temp_uvs.x*temp_uvs.y),
                                texture(tex, sample_pos).gb*i-(red_overlay*0.25), 1.0);;
}