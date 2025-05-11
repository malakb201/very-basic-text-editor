__major__ = 0
__minor__ = 1
__patch__ = 0
__build__ = 0

def get_version():
    return f"{__major__}.{__minor__}.{__patch__}.{__build__}"

def update_version(major=None, minor=None, patch=None, build=None):
    global __major__, __minor__, __patch__, __build__
    if major is not None: __major__ = major
    if minor is not None: __minor__ = minor
    if patch is not None: __patch__ = patch
    if build is not None: __build__ = build
    return get_version()