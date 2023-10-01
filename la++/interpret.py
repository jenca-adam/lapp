from .lappfile import parse_lapp

def execute(fn,argv):
    return parse_lapp(fn,argv).run()
