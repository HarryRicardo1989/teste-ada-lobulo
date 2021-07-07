from request_commands import RequestCommands


class AdaControl:
    def __init__(self):
        self.comando = RequestCommands()
        pass

    def set_ada_pos(self, pos_az, pos_el):
        self.comando.comand(f'ada pos -az {pos_az} -el {pos_el}')


