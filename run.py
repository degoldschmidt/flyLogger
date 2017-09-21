from flylogger import loadsheet
from flylogger import experiment

def main():
    mystocks = loadsheet.load_stocks()  ### collection object
    #myexperiment = experiment.setup()   ### set up experiment object (CLI)
    #myexperiment.save()                 ### saves experimental yaml file to given location

if __name__ == "__main__":
    main()
