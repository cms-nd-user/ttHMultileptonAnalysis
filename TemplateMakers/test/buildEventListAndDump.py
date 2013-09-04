#!/usr/bin/env python


#  
#
#




# imports 
import ROOT
import os
import sys


def readEventList (fileName):
    inputFile = open(fileName,'r')
    returnListOf3Tuples = []
    numLines = 0
    for iLine in inputFile.readlines():
        numLines = numLines + 1 
        cleanLine = iLine.strip()
        words = cleanLine.split(' ')
        if len(words) >= 3:
            returnListOf3Tuples.append( (int(words[0]), int(words[1]), int(words[2])) )
        else:
            print "Found words= ", len(words), " on line ", numLines
            exit (2)
    return returnListOf3Tuples

def buildEventList (inTree, eachEvent):

    newList = ROOT.TEventList("newList", "AnewList")
    numEvents =0
    lastSize =0 
    for (run, lumi, event) in eachEvent:
        numEvents = numEvents+1
        selectionString = "eventInfo_run == %d && eventInfo_lumi == %d && eventInfo_evt == %d" % (run,lumi,event)
        inTree.Draw(">>+newList", selectionString)
        currentSize = newList.GetN()
        print "Events %d, size of selectino %d" % (numEvents, currentSize )
        if currentSize - lastSize == 0:
            print "MISSING: {r} {l} {e} not in tree".format(r=run, l=lumi, e=event)

        lastSize = currentSize

    return newList

def buildCuts () :
    cutList = []
    cutList.append("((numPreselectedLeptons==2) || (-1.0 <= preselected_leptons_by_pt_3_lepMVA < 0.7))")
    cutList.append("min_mass_leplep > 12")
    cutList.append("preselected_leptons_by_pt_1_pt > 20 && preselected_leptons_by_pt_2_pt > 10")
    cutList.append("preselected_leptons_by_pt_2_pt > 20 && ((preselected_leptons_by_pt_1_pt + preselected_leptons_by_pt_2_pt + met_pt) > 100)")
    cutList.append("preselected_leptons_by_pt_1_lepMVA > 0.7 && preselected_leptons_by_pt_2_lepMVA > 0.7")
    cutList.append("preselected_leptons_by_pt_1_isMuon && preselected_leptons_by_pt_2_isMuon")
    cutList.append("((preselected_leptons_by_pt_1_tkCharge * preselected_leptons_by_pt_2_tkCharge) > 0)")
    cutList.append("preselected_leptons_by_pt_1_CERN_tight_charge && preselected_leptons_by_pt_2_CERN_tight_charge")
    cutList.append("numJets>=4")
    cutList.append("(numLooseBJets >= 2 || numMediumBJets >= 1)")
    cutList.append("isDoubleMuTriggerPass==1")
    cutList.append("(higgs_decay_type==2 || higgs_decay_type==3 || higgs_decay_type==4)")
    return cutList

def checkAllCuts (inTree, inCuts ) :
    yieldChecker = ROOT.TEventList("yieldChecker", "a yield")
    inTree.Draw(">>yieldChecker" )
    baselineYield = yieldChecker.GetN()
    for eachCut in inCuts:
        inTree.Draw(">>yieldChecker", eachCut)
        fraction = float (yieldChecker.GetN()) / float(baselineYield)
        print "Cut is ", eachCut, " --- yield is ", yieldChecker.GetN(), "  fraction is ", fraction
    

def main():

    print "Parsing event list..."
    runLumiEvent = readEventList("cernHasNDlacks.log")
    print "done reading, length is " , len(runLumiEvent)
    #print runLumiEvent

    inputRoot = ROOT.TFile('ntuple_ssTwoLep_unskimmed_ttH125.root')
    inputTree = inputRoot.Get('summaryTree')

    newList = buildEventList(inputTree, runLumiEvent)

    inputTree.SetEventList(newList)

    # TTree::Draw does not seem to return anything
    # instead, use the event lists
    #

    cuts = buildCuts()

    checkAllCuts (inputTree, cuts)

    print "Done"


if __name__ == "__main__":
    main ()

