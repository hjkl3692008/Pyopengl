#version 330 core

// Interpolated values from the vertex shaders
in vec2 UV;
in vec3 Position_worldspace;
in vec3 Normal_cameraspace;
in vec3 EyeDirection_cameraspace;
in vec3 LightDirection_cameraspace;

// Ouput data
out vec4 color;

// Values that stay constant for the whole mesh.
uniform sampler2D diffuse_texture;
uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;
uniform vec3 Light_location;
uniform float Material_shininess;
uniform vec4 Material_specular;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;

void main(){

	// Material properties
	vec4 MaterialDiffuseColor = texture( diffuse_texture, UV );

	// Distance to the light
	float distance = length( Light_location - Position_worldspace );

	// Normal of the computed fragment, in camera space
	vec3 n = normalize( Normal_cameraspace );
	// Direction of the light (from the fragment to the light)
	vec3 l = normalize( LightDirection_cameraspace );
	// Cosine of the angle between the normal and the light direction,
	// clamped above 0
	//  - light is at the vertical of the triangle -> 1
	//  - light is perpendicular to the triangle -> 0
	//  - light is behind the triangle -> 0
	float cosTheta = clamp( dot( n,l ), 0,1 );

	// Eye direction
	vec3 E = normalize(EyeDirection_cameraspace);
	// Reflection of the light
	//vec3 R = reflect(-l,n);
	//float cosAlpha = clamp( dot( E,R ), 0,1 );
    // half light
	vec3 half_light = normalize( l + E );
	// cos of half_light and normal
	float cosBeta = clamp( dot(half_light, n), 0, 1 );

    float LightPower = 2.0f;

	color =
		// Ambient : simulates indirect lighting
		Global_ambient * Material_ambient
		+ MaterialDiffuseColor * Material_ambient
		// Diffuse : "color" of the object
		+ MaterialDiffuseColor * Light_diffuse * cosTheta * LightPower
		// Specular : reflective highlight, like a mirror
		+ Light_specular * Material_specular * pow(cosBeta,Material_shininess) * LightPower;


}