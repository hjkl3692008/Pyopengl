#version 330 core

in vec3 Vertex_position;
in vec2 Vertex_texture_coordinate;
in vec3 Vertex_normal;

out vec2 UV;
out vec3 Position_worldspace;
out vec3 Normal_cameraspace;
out vec3 EyeDirection_cameraspace;
out vec3 LightDirection_cameraspace;

uniform mat4 MVP; //Project * View * Model
uniform mat4 ViewMatrix; // View matrix
uniform mat4 ModelMatrix; // Model matrix
uniform vec3 Light_location;
uniform vec3 LOCATION_OFFSET = vec3(0.0,0.0,0.0);
void main(){

	// Output position of the vertex, in clip space : MVP * position
	gl_Position =  MVP * vec4(Vertex_position+LOCATION_OFFSET,1);

	// Position of the vertex, in worldspace : ModelMatrix * position
	Position_worldspace = (ModelMatrix * vec4(Vertex_position,1)).xyz;

	// Vector that goes from the vertex to the camera, in camera space.
	// In camera space, the camera is at the origin (0,0,0).
	vec3 vertexPosition_cameraspace = ( ViewMatrix * ModelMatrix * vec4(Vertex_position+LOCATION_OFFSET,1)).xyz;
	EyeDirection_cameraspace = vec3(0,0,0) - vertexPosition_cameraspace;

	// Vector that goes from the vertex to the light, in camera space. ModelMatrix is ommited because it's identity.
	vec3 LightPosition_cameraspace = ( ViewMatrix * vec4(Light_location+LOCATION_OFFSET,1)).xyz;
	LightDirection_cameraspace = LightPosition_cameraspace - vertexPosition_cameraspace;

	// Normal of the the vertex, in camera space
	Normal_cameraspace = ( ViewMatrix * ModelMatrix * vec4(Vertex_normal,0)).xyz;

	// UV of the vertex. No special space for this one.
	UV = Vertex_texture_coordinate;
}

