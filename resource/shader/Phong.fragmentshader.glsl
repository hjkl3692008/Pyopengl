uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;
uniform vec3 Light_location;
uniform float Material_shininess;
uniform vec4 Material_specular;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;
varying vec3 baseNormal;

vec2 phong_weightCalc(
    in vec3 light_pos, // light position
    in vec3 half_light, // half-way vector between light and view
    in vec3 frag_normal, // geometry normal
    in float shininess
) {
    // returns vec2( diffuse_mult, specular_mult )
    float diffuse_mult = max( 0.0, dot(
        frag_normal, light_pos
    ));
    float specular_mult = 0.0;
    if (diffuse_mult > -.05) {
        specular_mult = pow(max(0.0,dot(
            half_light, frag_normal
        )), shininess);
    }
    return vec2( diffuse_mult, specular_mult);
}

void main() {
    // normalized eye-coordinate Light location
    vec3 EC_Light_location = normalize(
        gl_NormalMatrix * Light_location
    );
    vec3 eye_direction = vec3( 0,0,-1 );
    // half-vector calculation
    vec3 Light_half = normalize(
        EC_Light_location + eye_direction
    );
    vec2 weights = phong_weightCalc(
        EC_Light_location, // L
        Light_half,  // H
        baseNormal,  // N
        Material_shininess  // n
    );
    gl_FragColor = clamp(
    (
        (Global_ambient * Material_ambient) // global ambient
        + (Light_ambient * Material_ambient) // local ambient
        + (Light_diffuse * Material_diffuse * weights.x) // local diffuse
        + (Light_specular * Material_specular * weights.y) // local specular
    ), 0.0, 1.0);
}
