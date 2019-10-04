import sys, os
import settings
from core import managedb, commandController

def runCommand(run):
    comandsController = commandController.ComandsController()
    comandsController.run(run)
    return

run = sys.argv
runCommand(run)
