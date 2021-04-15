
import os
father_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class handle_body():
    def __init__(self):
        self.path=father_path+'/config/body'
