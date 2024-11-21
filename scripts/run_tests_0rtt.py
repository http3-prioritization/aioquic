import subprocess
import random
import string 
import os

# need to run setup.py first to make sure all our changes are compiled before running
# if you didn't make changes to aioquic, you can comment this step out
# need to run this from inside the root dir
# also need to switch the venv first: source .venv/bin/activate
# so do python3 scripts/run_tests_0rtt.py

directoryName = "aioquic"
logDirectoryName = "aioquic"

print("Compiling...")
process = subprocess.run("{}".format("python3 /srv/"+directoryName+"/setup.py install"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

if process.returncode is not 0:
    print ("ERROR in compilation: ", process.returncode, " != 0?")
    print ( process.stderr )

print("Compilation done!")

nozerorttendpoints = []

basecommand = "python3 /srv/"+directoryName+"/examples/http3_client.py -v"

class Endpoint:
    def __init__(self, url, name):
        self.url = url
        self.name = name

runname = ""
ticketNumber = 0
# storeTicket = False
# readTicket = False

# proper_endpoints = [
#     Endpoint("https://quic.aiortc.org/{}", "akamai"),
# ]

# def run_single(size, amplification_factor, testname):

#     for endpoint in proper_endpoints:
#         url = endpoint.url.format(str(size))

#         ticket = ""
#         ticketFileName = ""
#         if storeTicket:
#             ticket = " --session-ticket-write /srv/" + directoryName + "/tickets/" + endpoint.name + str(ticketNumber) + ".ticket "
#             ticketFileName = "1RTT_"
#         elif readTicket:
#             ticket = " --session-ticket-read /srv/" + directoryName + "/tickets/" + endpoint.name + str(ticketNumber) + ".ticket "
#             ticketFileName = "0RTT_"


#         cmd = basecommand + " " + ticket + "--quic-log /srv/"+logDirectoryName+"/qlog/run"+ runname + "_" + testname + "_"  + ticketFileName + endpoint.name + ".qlog " + "--amplification-factor " + str(amplification_factor) + " " + url
#         print ("Executing ", cmd)
#         run_command ( cmd )

def run_single_endpoint(url, doZeroRtt, amplification_factor, testname, endpointName):

    ticketFilepath = "/srv/" + directoryName + "/tickets/" + endpointName + "_" + testname + str(ticketNumber) + ".ticket"

    runType = "0rtt"

    if not doZeroRtt:
        runType = "1rtt"
        # want to make sure any existing ticket data is gone so we have to create a new one
        # otherwise we might fail to get a ticket, and try to reuse an old one for the same ticketNumber run
        if os.path.exists(ticketFilepath):
            os.remove(ticketFilepath)
            print(f"The existing ticket at {ticketFilepath} has been deleted.")

    # cmd = basecommand + " " + ticket + "--quic-log /srv/"+logDirectoryName+"/qlog/run"+ runname + "_" + testname + "_" + ticketFileName + endpointName + ".qlog " + "--amplification-factor " + str(amplification_factor) + " \"" + url + "\""
    
    cmd = basecommand + " --session-ticket " + ticketFilepath + " --quic-log /srv/"+logDirectoryName+"/qlog/run"+ runname + "_" + testname + "_" + runType + "_" + endpointName + str(ticketNumber) + ".qlog "
    
    if doZeroRtt:
        cmd += "--zero-rtt "

    cmd += "\"" + url + "\""
    
    print ("Executing ", cmd)
    run_command ( cmd )

def run_command(cmd):
    process = subprocess.run("{}".format(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if ( len(process.stdout) > 0 ):
        if process.stdout.find("EARLY_DATA NOT ACCEPTED") >= 0:
            nozerorttendpoints.append( cmd )
        elif process.stdout.find("so not doing 0rtt") >= 0:
            nozerorttendpoints.append( cmd )

        print ( process.stdout )

    if len(process.stderr) is not 0 or process.returncode is not 0:
        if process.stderr.find("EARLY_DATA NOT ACCEPTED") >= 0:
            nozerorttendpoints.append( cmd )
        elif process.stderr.find("so not doing 0rtt") >= 0:
            nozerorttendpoints.append( cmd )

        # print ("Potential ERROR in process: ", process.returncode, " != 0?")
        print ( process.stderr )
        # print( "stderr length was %d", len(process.stderr) )

ticketNumber = 3 # so tickets don't get overridden if we want to prep all ampfactor tests at once
# set both to False for addressFixed mode (run 1rtt and 0rtt back-to-back)
# set first storeTicket = True, then readTicket = True for addressChange mode 
# (change network in between of course. We used a VPN, but you could also copy over the tickets)
# storeTicket = False
# readTicket = False

# run_single_endpoint( "https://www.internetonmars.org/akamai/tests/earlydata/small.jpg", False,  0, "smallimgcached", "akamai" )
# run_single_endpoint( "https://www.internetonmars.org/akamai/tests/earlydata/small.jpg", True,   0, "smallimgcached", "akamai" )


run_single_endpoint( "https://www.internetonmars.org/akamai/tests/earlydata/small.jpg?test=123", False,  0, "smallimgcachedquery", "akamai" )
run_single_endpoint( "https://www.internetonmars.org/akamai/tests/earlydata/small.jpg?test=123", True,   0, "smallimgcachedquery", "akamai" )