from structures import *
from utils import *

def initModule(cod):
    cod.botcommands["TEST"] = [test]

def destroyModule(cod):
    del cod.botcommands["TEST"]

def test(cod, line, splitline, source, destination):
    reply(cod, source, destination, "Hello!")
