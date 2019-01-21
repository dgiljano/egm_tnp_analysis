#############################################################
########## General settings
#############################################################

# Runs to include
runs = "BCEF"

# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# flag to be Tested
flags = {
    'passingVeto94X'    : '(passingVeto94X   == 1)',
    'passingLoose94X'   : '(passingLoose94X  == 1)',
    'passingMedium94X'  : '(passingMedium94X == 1)',
    'passingTight94X'   : '(passingTight94X  == 1)',
    'passingMVA94Xwp80iso' : '(passingMVA94Xwp80iso == 1)',
    'passingMVA94Xwp90iso' : '(passingMVA94Xwp90iso == 1)',
    'passingMVA94Xwp80noiso' : '(passingMVA94Xwp80noiso == 1)',
    'passingMVA94Xwp90noiso' : '(passingMVA94Xwp90noiso == 1)',
    'passingMVA94XwpHZZiso' : '(passingMVA94XwpHZZisoV2 == 1 && fabs(el_sip) < 4 && fabs(el_dz) < 1 && fabs(el_dxy) < 0.5)',
    }

baseOutDir = 'results/egm2017/tnpEleID/run{0}/'.format(runs)

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

samplesDef = {
    'data'   : tnpSamples.egm2017['data_Run{0}_2017'.format(runs[0])].clone(),
    'mcNom'  : tnpSamples.egm2017['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.egm2017['DY_amcatnlo'].clone(),
    'tagSel' : tnpSamples.egm2017['DY_madgraph'].clone(),
}

## can add data sample easily
for r in runs[1:]:
    samplesDef['data'].add_sample( tnpSamples.egm2017['data_Run{0}_2017'.format(r)] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking periods
#weightName = 'weights_2017_run{0}.totWeight'.format(runs)
weightName = 'weights_2017_runBCDEF.totWeight'.format(runs)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
# if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_180130/Moriond18_V1/PU/mc-V2-customW/DY_madgraph_ele.pu.puTree.root')
# if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_180130/Moriond18_V1/PU/mc-V2-customW/DY_amcatnlo_Moriond18_ele.pu.puTree.root')
# if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_180130/Moriond18_V1/PU/mc-V2-customW/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree("/data_CMS/cms/giljanovic/2017_data/PU/DY_madgraph_ele.pu.puTree.root")
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree("/data_CMS/cms/giljanovic/2017_data/PU/DY_amcatnlo_ele.pu.puTree.root")
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree("/data_CMS/cms/giljanovic/2017_data/PU/DY_madgraph_ele.pu.puTree.root")


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   # very low pt
   [{ 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 1.5, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [7,10] },],
   # low pt
   [{ 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 0.8, 1.5, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,15] },],
   # medium pt
   [{ 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.5, -0.8, 0.0, 0.8, 1.5, 2.0, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [15,20,35,50,100] }, ],
   # high pt
   [{ 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 1.5, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [100, 500] },],
   # # gaps
   # [{ 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 2.5] },
    # { 'var' : 'el_pt' , 'type': 'float', 'bins': [7,15,35,500] }],
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'
addCutLowPt = 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = {}
for i in range(39):
    additionalCuts[i] = ""

for i in range(13):
    if additionalCuts[i] == "":
        additionalCuts[i] = addCutLowPt
    else:
        additionalCuts[i] = additionalCuts[i] + " && " + addCutLowPt

# No gap
for i in range(39):
    if additionalCuts[i] == "":
        additionalCuts[i] = "!el_isGap"
    else:
        additionalCuts[i] = additionalCuts[i] + " && !el_isGap"

# # Gap cut
# for i in range(44, 47):
    # if additionalCuts[i] == "":
        # additionalCuts[i] = "el_isGap"
    # else:
        # additionalCuts[i] = additionalCuts[i] + " && el_isGap"

# # low pt gap
# additionalCuts[44] = additionalCuts[44] + " && " + addCutLowPt

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.5,0.8]",
    #"acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    "acmsF[0.]","betaF[999.]","gammaF[0.1, -2, 2]","peakF[90.0]", # exponential
    #"acmsF[50]","betaF[0.079]","gammaF[0.1]","peakF[90.]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    "acmsF[0.]","betaF[999.]","gammaF[0.1, -2, 2]","peakF[90.0]", # exponential
    ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "aP[0,0,1000]",
    "bP[0,-100,100]",
    "cP[0,-100,100]",
    "aF[0,0,1000]",
    "bF[0,-100,100]",
    "cF[0,-100,100]",
    #"alphaP[0.,-5.,5.]",
    #"alphaF[0.,-5.,5.]",
    ]
