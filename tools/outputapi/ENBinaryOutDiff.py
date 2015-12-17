'''Compares Two EPANET binary output files.Author: Bryant E. McDonnellDate: 12/16/2015Compares the absolute value of two values against a given threshold value.*******************Command Line Arguments:python <OutDiff.py> <*.out 1> <*.out 2> Returns True / False (Pass / Fail, respectively)*******************'''import sysimport osfrom math import logfrom ENOutputWrapper import *def BinCompare(args):    # Some Error Checking for Command Line Arguments....    if len(args) < 3:        raise Exception("Not Enough Input Arguments: python <ENBinaryOutDiff.py> <*.out 1> <*.out 2>")#    if not args[1].endswith('.out') or not args[2].endswith('.out'):#        raise Exception("Wrong file extension: python <ENBinaryOutDiff.py> <*.out 1> <*.out 2>")    print(sys.argv[1],sys.argv[2])        dllLoc = ''    if (sys.platform == 'linux2' or sys.platform == 'darwin'):        dllLoc = os.getcwd() + '/libENBinaryOut.so'    else:        raise Exception("only implemented on mac/linux")        BinFile1 = OutputObject(dllLoc)    BinFile1.OpenOutputFile(args[1])    BinFile1.get_NetSize()    BinFile1.get_Times()    BinFile2 = OutputObject(dllLoc)    BinFile2.OpenOutputFile(args[2])    ####ENR_NodeAttribute;    ##ENR_demand   = 0    ##ENR_head     = 1    ##ENR_pressure = 2    ##ENR_quality  = 3    NumberOfNodeAttr = 4    ####ENR_LinkAttribute;    ##ENR_flow         = 0    ##ENR_velocity     = 1    ##ENR_headloss     = 2    ##ENR_avgQuality   = 3    ##ENR_status       = 4    ##ENR_setting      = 5    ##ENR_rxRate       = 6    ##ENT_frctnFctr    = 7    NumberOfLinkAttr = 8    NumberOfPeriods = BinFile1.numPeriods    # Set Tolerances for each attribute    # demand, head, pressure, quality    NodeAttributeTolerances = [1e-6, 1e-6, 1e-6, 1e-6]    # flow, velocity, headloss, avgQuality, status, setting, rxRate, frctnFctr    LinkAttributeTolerances = [1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6]    #Compare Node Attributes    for nodeAttrInd in range(NumberOfNodeAttr):        for TSind in range(NumberOfPeriods):            #Get 1 attribute for all nodes at time t            NodeAttributeOut1 = BinFile1.get_NodeAttribute(nodeAttrInd, TSind)            #Get 1 attribute for all nodes at time t            NodeAttributeOut2 = BinFile2.get_NodeAttribute(nodeAttrInd, TSind)            for Nodeind, NodeAttrVal in enumerate(NodeAttributeOut1):                if abs(NodeAttrVal - NodeAttributeOut2[Nodeind]) > 0:                    diff = abs(NodeAttrVal - NodeAttributeOut2[Nodeind] )                    if diff > NodeAttributeTolerances[nodeAttrInd]:                    	print ("Node ", Nodeind, " attribute ", nodeAttrInd, "exceeded tolerance")                        return False    #Compare Link Attributes                    for linkAttrInd in range(NumberOfLinkAttr):        for TSind in range(NumberOfPeriods):            #Get 1 attribute for all links at time t            LinkAttributeOut1 = BinFile1.get_NodeAttribute(linkAttrInd, TSind)            #Get 1 attribute for all links at time t            LinkAttributeOut2 = BinFile2.get_NodeAttribute(linkAttrInd, TSind)            for linkind, LinkAttrVal in enumerate(LinkAttributeOut1):                if abs(LinkAttrVal - LinkAttributeOut2[linkind]) > 0:                    diff = abs(LinkAttrVal - LinkAttributeOut2[linkind] )                    if diff > LinkAttributeTolerances[linkAttrInd]:                    	print ("Link ", linkind, " attribute ", linkAttrInd, "exceeded tolerance")                        return False    return Trueif __name__ == '__main__':    if(BinCompare(sys.argv)):    	sys.exit(0)    else:        sys.exit(1)