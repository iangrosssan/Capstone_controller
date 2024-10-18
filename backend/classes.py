import libximc.highlevel as ximc

class AxisManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AxisManager, cls).__new__(cls)
            cls._instance.axes = []
        return cls._instance

    def set_axes(self, uris):
        self.axes = [ximc.Axis(uri) for uri in uris]