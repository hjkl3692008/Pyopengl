Phong_uniform_default_parameter = {'Global_ambient': [0.05, 0.05, 0.05, 0.1],
                                   'Light_ambient': [0.1, 0.1, 0.1, 1.0],
                                   'Light_diffuse': [0.25, 0.25, 0.25, 1],
                                   'Light_specular': [0.0, 1.0, 0.0, 1.0],
                                   'Light_location': [-5.0, -5.0, -5.0],
                                   'Material_ambient': [0.1, 0.1, 0.1, 1.0],
                                   'Material_diffuse': [0.15, 0.15, 0.15, 1.0],
                                   'Material_specular': [1.0, 1.0, 1.0, 1.0],
                                   'Material_shininess': [0.95]
                                   }

Gouraud_uniform_default_parameter = {'Global_ambient': [0.05, 0.05, 0.05, 0.1],
                                     'Light_ambient': [0.1, 0.1, 0.1, 1.0],
                                     'Light_diffuse': [0.25, 0.25, 0.25, 1],
                                     'Light_specular': [0.0, 1.0, 0.0, 1.0],
                                     'Light_location': [-5.0, -5.0, -5.0],
                                     'Material_ambient': [0.1, 0.1, 0.1, 1.0],
                                     'Material_diffuse': [0.15, 0.15, 0.15, 1.0],
                                     'Material_specular': [1.0, 1.0, 1.0, 1.0],
                                     'Material_shininess': [0.95]
                                     }

Flat_uniform_default_parameter = {'Global_ambient': [0.05, 0.05, 0.05, 0.1],
                                  'Light_ambient': [0.1, 0.1, 0.1, 1.0],
                                  'Light_diffuse': [0.25, 0.25, 0.25, 1],
                                  'Light_specular': [0.0, 1.0, 0.0, 1.0],
                                  'Light_location': [-5.0, -5.0, -5.0],
                                  'Material_ambient': [0.1, 0.1, 0.1, 1.0],
                                  'Material_diffuse': [0.15, 0.15, 0.15, 1.0],
                                  'Material_specular': [1.0, 1.0, 1.0, 1.0],
                                  'Material_shininess': [0.95]
                                  }

Phong_attribute_default_parameter = {'Vertex_position': 0,
                                     'Vertex_normal': 0
                                     }
Gouraud_attribute_default_parameter = {'Vertex_position': 0,
                                       'Vertex_normal': 0
                                       }
Flat_attribute_default_parameter = {'Vertex_position': 0,
                                    'Vertex_normal': 0
                                    }

parameter_dict = {
    'Phong.vertexshader.glsl': Phong_uniform_default_parameter,
    'Gouraud.vertexshader.glsl': Gouraud_uniform_default_parameter,
    'Flat.vertexshader.glsl': Flat_uniform_default_parameter,
    'Phong.fragmentshader.glsl': Phong_attribute_default_parameter,
    'Gouraud.fragmentshader.glsl': Gouraud_attribute_default_parameter,
    'Flat.fragmentshader.glsl': Flat_attribute_default_parameter
}
