# light parameter
basic_light_dict = {'Global_ambient': [0.05, 0.05, 0.05, 0.1],
                    'Light_ambient': [0.1, 0.1, 0.1, 1.0],
                    'Light_diffuse': [0.25, 0.25, 0.25, 1],
                    'Light_specular': [0.0, 1.0, 0.0, 1.0],
                    'Light_location': [-5.0, -5.0, -5.0],
                    'Material_ambient': [0.1, 0.1, 0.1, 1.0],
                    'Material_diffuse': [0.15, 0.15, 0.15, 1.0],
                    'Material_specular': [1.0, 1.0, 1.0, 1.0],
                    'Material_shininess': [0.95]
                    }

Phong_uniform_default_parameter = basic_light_dict
Gouraud_uniform_default_parameter = basic_light_dict
Flat_uniform_default_parameter = basic_light_dict
Texture_uniform_default_parameter = basic_light_dict
Texture_uniform_default_parameter.update({'Light_specular': [0.2, 0.2, 0.2, 1.0],
                                          'MVP': None,
                                          'ModelMatrix': None,
                                          'ViewMatrix': None,
                                          'diffuse_texture': None,
                                          'LOCATION_OFFSET': None})

# attribute
basic_attribute_dict = {'Vertex_position': 0,
                        'Vertex_normal': 0,
                        'Vertex_texture_coordinate': 0
                        }

Phong_attribute_default_parameter = basic_attribute_dict
Gouraud_attribute_default_parameter = basic_attribute_dict
Flat_attribute_default_parameter = basic_attribute_dict
Texture_attribute_default_parameter = basic_attribute_dict

parameter_dict = {
    'Phong.vertexshader.glsl': Phong_uniform_default_parameter,
    'Gouraud.vertexshader.glsl': Gouraud_uniform_default_parameter,
    'Flat.vertexshader.glsl': Flat_uniform_default_parameter,
    'Texture.vertexshader.glsl': Texture_uniform_default_parameter,
    'Phong.fragmentshader.glsl': Phong_attribute_default_parameter,
    'Gouraud.fragmentshader.glsl': Gouraud_attribute_default_parameter,
    'Flat.fragmentshader.glsl': Flat_attribute_default_parameter,
    'Texture.fragmentshader.glsl': Texture_attribute_default_parameter,
}
