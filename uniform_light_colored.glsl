#version 330 core
uniform sampler2D image;
uniform vec3 luminosity;

in vec2 fragmentTexCoord;
out vec4 color;

void main() {
    color = texture(image, fragmentTexCoord);
    color.rgb = color.rgb * luminosity;
}