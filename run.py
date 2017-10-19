from flylogger import authorize
from flylogger import experiment
from flylogger import load
from flylogger import app

def main():
    my_client = authorize.me()
    app.run(client=my_client)
    #mystocks = loadef list_ssheets(self)d.stocks()  ### collection object
    #myexperiment = experiment.setup()   ### set up experiment object (CLI)
    #myexperiment.save()                 ### saves experimental yaml file to given location

if __name__ == "__main__":
    main()
