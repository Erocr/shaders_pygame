#version 330 core
uniform sampler2D image;
uniform float luminosity;

uniform float luminosity_slope;
uniform vec3 pointlights[20];
uniform int nbLights;

uniform sampler2D normal_map;

in vec2 fragmentTexCoord;
out vec4 color;

void main() {
    float pixelLuminosity = luminosity;

    vec3 normal = texture(normal_map, fragmentTexCoord).rgb;
    normal = normal * 2 - 1;
    vec3 pixelPos = vec3(fragmentTexCoord, 0);
    for (int i=0; i < nbLights && i < 20; i++) {
        vec3 lightPos = vec3(pointlights[i].xy, 0.1);
        vec3 lightDir = normalize(lightPos - pixelPos);
        float pointingLightFactor = max(dot(lightDir, normal), 0);
        float d = distance(pointlights[i].xy, fragmentTexCoord);
        pixelLuminosity += max(pointlights[i].z - d * luminosity_slope, 0) * pointingLightFactor;
    }

    color = texture(image, fragmentTexCoord);
    color.rgb = color.rgb * pixelLuminosity;
}