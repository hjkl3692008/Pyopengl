from model import windows
from model.cow import Cow
from model import Cow_Animated
from model import Cow_Animated2
from tools import shader_tools as st
import numpy as np

if __name__ == "__main__":
    win = windows.Window()

    win.init()

    # cow1 = Cow(vertex_shaders=[st.FLAT_VERTEX_SHADER], fragment_shaders=[st.FLAT_FRAGMENT_SHADER])
    # cow2 = Cow(vertex_shaders=[st.GOURAUD_VERTEX_SHADER], fragment_shaders=[st.GOURAUD_FRAGMENT_SHADER])
    # cow3 = Cow()
    # win.add_object(cow1, location=np.array([0.0, 0.0, 4.0]))
    # win.add_object(cow2)
    # win.add_object(cow3, location=np.array([0.0, 0.0, -4.0]))

    # cow = Cow(vertex_shaders=[st.TEXTURE_VERTEX_SHADER], fragment_shaders=[st.TEXTURE_FRAGMENT_SHADER],
    #           texture_name='wood.jpg')
    # win.add_object(cow)

    cow = Cow_Animated2(vertex_shaders=[st.ANIMATED_VERTEX_SHADER], fragment_shaders=[st.ANIMATED_FRAGMENT_SHADER],
              texture_name='wood.jpg')
    win.add_object(cow)
    win.run()

    # Cow_Animated().ContextMainLoop()
