#version 330 core
uniform sampler2D image;
uniform float luminosity;

uniform float luminosity_slope;
uniform vec3 pointlights[20];
uniform int nbLights;

in vec2 fragmentTexCoord;
out vec4 color;

void main() {
    float pixelLuminosity = luminosity;

    for (int i=0; i < nbLights && i < 20; i++) {
        float d = distance(pointlights[i].xy, fragmentTexCoord);
        pixelLuminosity += max(pointlights[i].z - d * luminosity_slope, 0);
    }

    color = texture(image, fragmentTexCoord);
    color.rgb = color.rgb * pixelLuminosity;
}