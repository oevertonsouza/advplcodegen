# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, commandController

def runCommand(run):
    comandsController = commandController.ComandsController()
    comandsController.run(run)
    return

run = sys.argv
runCommand(run)
