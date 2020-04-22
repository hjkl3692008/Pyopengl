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

	// Material diffuse color (texture)
	vec4 MaterialDiffuseColor = texture( diffuse_texture, UV );

	// Distance to the light
	float distance = length( Light_location - Position_worldspace );

	// Normal of the vertex, in camera space
	vec3 n = normalize( Normal_cameraspace );
	// Direction of the light, in camera space
	vec3 l = normalize( LightDirection_cameraspace );
	// Cosine of the angle between the normal and the light direction,
	float cosTheta = clamp( dot( n,l ), 0,1 );

	// Eye direction, in camera space
	vec3 E = normalize(EyeDirection_cameraspace);
	// we have 2 method to calculate angle
	// 1. Cosine of the angle between the reflection and Eye direction
	// Reflection of the light
	//vec3 R = reflect(-l,n);
	//float cosAlpha = clamp( dot( E,R ), 0,1 );
	// 2. Cosine of the angle between the half light and normal
    // half light
	vec3 half_light = normalize( l + E );
	// cos of half_light and normal
	float cosBeta = clamp( dot(half_light, n), 0, 1 );

    float lightPower = 2.0;

	color =
		// Ambient : simulates indirect lighting
		// global ambient
		Global_ambient * Material_ambient
		// local ambient
		+ MaterialDiffuseColor * Material_ambient
		// Diffuse : color of the object
		+ MaterialDiffuseColor * Light_diffuse * cosTheta * lightPower
		// Specular : reflective highlight
		+ Light_specular * Material_specular * pow(cosBeta,Material_shininess) * lightPower;

}