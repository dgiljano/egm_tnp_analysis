import ROOT as rt
import math
from fitUtils import *
#from fitSimultaneousUtils import *
    
def removeNegativeBins(h):
    for i in xrange(h.GetNbinsX()):
	if (h.GetBinContent(i) < 0):
            h.SetBinContent(i, 0)


def makePassFailHistograms( sample, flag, bindef, var ):
    ## open rootfile
    tree = rt.TChain(sample.tree)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)
    
    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    ## open outputFile
    outfile = rt.TFile(sample.histFile,'recreate')
    hPass = []
    hFail = []
    for ib in range(len(bindef['bins'])):
        
        hPass.append(rt.TH1D('%s_Pass' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hFail.append(rt.TH1D('%s_Fail' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hPass[ib].Sumw2()
        hFail[ib].Sumw2()
    
        cuts = bindef['bins'][ib]['cut']
        if sample.mcTruth :
            cuts = '%s && mcTrue==1' % cuts
        if not sample.cut is None :
            cuts = '%s && %s' % (cuts,sample.cut)
                
        if sample.isMC :
            cutPass = '( %s &&  %s ) * %s ' % (cuts, flag, sample.weight)
            cutFail = '( %s && !%s ) * %s ' % (cuts, flag, sample.weight)
        else:
            cutPass = '( %s &&  %s )' % (cuts, flag)
            cutFail = '( %s && !%s )' % (cuts, flag)
        
        tree.Draw('%s >> %s' % (var['name'],hPass[ib].GetName()),cutPass,'goff')
        tree.Draw('%s >> %s' % (var['name'],hFail[ib].GetName()),cutFail,'goff')

        
        removeNegativeBins(hPass[ib])
        removeNegativeBins(hFail[ib])

        hPass[ib].Write(hPass[ib].GetName())
        hFail[ib].Write(hFail[ib].GetName())

        passI = hPass[ib].Integral()
        failI = hFail[ib].Integral()
        eff = 0
        if passI > 0 :
            eff = passI / (passI+failI)
        print cuts
        print '    ==> pass: %.1f ; fail : %.1f : eff: %1.3f' % (passI,failI,eff)
    outfile.Close()




def histPlotter( filename, tnpBin, plotDir ):
    print 'opening ', filename
    print '  get canvas: ' , '%s_Canv' % tnpBin['name']
    rootfile = rt.TFile(filename,"read")

    c = rootfile.Get( '%s_Canv' % tnpBin['name'] )
    c.Print( '%s/%s.png' % (plotDir,tnpBin['name']))


def computeEffi( n1,n2,e1,e2):
    eff = []
    eff.append(n1/(n1+n2))
    eff.append(1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2))
    return eff


import os.path
def getAllEffi( info, bindef ):
    effis = {}
    if not info['mcNominal'] is None and os.path.isfile(info['mcNominal']):
        rootfile = rt.TFile( info['mcNominal'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        nP = hP.Integral()
        nF = hF.Integral()
        eP = math.sqrt(hP.GetEntries())/hP.GetEntries() * nP
        eF = math.sqrt(hF.GetEntries())/hF.GetEntries() * nF

        effis['mcNominal'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcNominal'] = [-1,-1]

    if not info['tagSel'] is None and os.path.isfile(info['tagSel']):
        rootfile = rt.TFile( info['tagSel'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        nP = hP.Integral()
        nF = hF.Integral()

        eP = math.sqrt(hP.GetEntries())/hP.GetEntries() * nP
        eF = math.sqrt(hF.GetEntries())/hF.GetEntries() * nF
        if eP < 0.001 : eP = 0.001
        if eF < 0.001 : eF = 0.001

        effis['tagSel'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['tagSel'] = [-1,-1]
        
    if not info['mcAlt'] is None and os.path.isfile(info['mcAlt']):
        rootfile = rt.TFile( info['mcAlt'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        nP = hP.Integral()
        nF = hF.Integral()

        eP = math.sqrt(hP.GetEntries())/hP.GetEntries() * nP
        eF = math.sqrt(hF.GetEntries())/hF.GetEntries() * nF
        if eP < 0.001 : eP = 0.001
        if eF < 0.001 : eF = 0.001

        effis['mcAlt'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcAlt'] = [-1,-1]

    if not info['dataNominal'] is None and os.path.isfile(info['dataNominal']) :
        rootfile = rt.TFile( info['dataNominal'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )
        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        if eP < 0.001 : eP = 0.001
        if eF < 0.001 : eF = 0.001

        effis['dataNominal'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else:
        effis['dataNominal'] = [-1,-1]
    if not info['dataAltSig'] is None and os.path.isfile(info['dataAltSig']) :
        rootfile = rt.TFile( info['dataAltSig'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()
        if eP < 0.001 : eP = 0.001
        if eF < 0.001 : eF = 0.001

        effis['dataAltSig'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else:
        effis['dataAltSig'] = [-1,-1]

    if not info['dataAltBkg'] is None and os.path.isfile(info['dataAltBkg']):
        rootfile = rt.TFile( info['dataAltBkg'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()
        if eP < 0.001 : eP = 0.001
        if eF < 0.001 : eF = 0.001

        effis['dataAltBkg'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else:
        effis['dataAltBkg'] = [-1,-1]
    return effis
