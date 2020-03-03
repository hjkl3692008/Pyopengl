from model import windows
from model.cow import Cow
from tools import shader_tools as st
import numpy as np

if __name__ == "__main__":
    win = windows.Window()

    win.init()

    cow1 = Cow(vertex_shaders=[st.FLAT_VERTEX_SHADER], fragment_shaders=[st.FLAT_FRAGMENT_SHADER])
    cow2 = Cow(vertex_shaders=[st.GOURAUD_VERTEX_SHADER], fragment_shaders=[st.GOURAUD_FRAGMENT_SHADER])
    cow3 = Cow()
    win.add_object(cow1, location=np.array([0.0, 0.0, 4.0]))
    win.add_object(cow2)
    win.add_object(cow3, location=np.array([0.0, 0.0, -4.0]))

    win.run()
