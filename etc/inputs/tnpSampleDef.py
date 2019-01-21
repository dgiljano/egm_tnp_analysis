from libPython.tnpClassUtils import tnpSample

### qll stat
#eosDir1 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/v1/'
#eosDir2 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/v2/'
#eosDirREC = 'eos/cms/store/group/phys_egamma/tnp/80X/RecoSF/RECOSFs_2016/'
#eosWinter17 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/Moriond17_v1/'
#eosMoriond18 = '/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_01292018/Moriond18_V1/'
#eos2018Data_V1 = '/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_05122018/2018Data_V1/'
#eos2018Data_V3 = '/eos/cms/store/group/phys_egamma/soffi/TnP/ntuples_06152018/2018Data_1/'

#Moriond18_94X = {
egm2017 = {
    ### MiniAOD TnP for IDs scale factors
    "DY_madgraph"   : tnpSample("DY_madgraph","/data_CMS/cms/giljanovic/2019_1_15/mc/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/" + "DY1JetsToLL_M50_madgraphML_all.root", isMC = True, nEvts = 1),    
#    "DY_madgraph2"  : tnpSample("/data_CMS/cms/giljanovic/2019_1_15/mc/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DY1JetsToLL_M50_madgraphMLM_ext1/" + "DY1JetsToLL_M50_madgraphMLM_ext1.root", isMC = True, nEvts = -1)
    "DY_amcatnlo"   : tnpSample("DY_amcatnlo","/data_CMS/cms/giljanovic/2019_1_15/mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M50_amcatnloFXFX/" + "DYJetsToLL_M50_amcatnloFXFX.root", isMC = True, nEvts = 1), 
    
    
    'data_RunB_2017' : tnpSample("data_RunB_2017","/data_CMS/cms/giljanovic/2019_1_15/data/SingleElectron/crab_RunB_2017/" + "data_RunB_2017.root" , lumi = 4.891 ),
    'data_RunC_2017' : tnpSample("data_RunC_2017","/data_CMS/cms/giljanovic/2019_1_15/data/SingleElectron/crab_RunC_2017_retry/" +  "data_RunC_2017.root", lumi = 9.9 ),
#    'data_Run2017D' : tnpSample('data_Run2017D' , eosMoriond18 + 'data/TnPTree_17Nov2017_RunD.root' , lumi = 4.36 ),
    'data_RunE_2017' : tnpSample("data_RunE_2017","/data_CMS/cms/giljanovic/2019_1_15/data/SingleElectron/crab_RunE_2017_retry/" + "data_RunE_2017.root" , lumi = 9.53 ),
    'data_RunF_2017' : tnpSample("data_RunF_2017","/data_CMS/cms/giljanovic/2019_1_15/data/SingleElectron/crab_RunF_2017/" + "data_RunF_2017.root" , lumi = 13.96 ),

    }

#Data2018_10_1_X = {

#    'DY_madgraph'          : tnpSample('DY_madgraph',
#                                       eosMoriond18 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_all.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_madgraph_2018_30p' : tnpSample('DY_madgraph_2018_30p',
#                                       eos2018Data_V3 + 'mc/TnP_DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_30pStat_all.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo_2018' : tnpSample('DY_amcatnlo_Moriond18',
#                                       eosMoriond18 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_all.root',
#                                       isMC = True, nEvts =  -1 ),

#    'data_2018_RunA_v123' : tnpSample('data_2018_RunA_v123' , eos2018Data_V3 + 'data/TnP_Prompt2018_RunA_v123_selectedRuns.root' , lumi = 0 ),#FIXME so far all the integrated value of the lumi is assigned to runb, still need to compute individual run lumi
#    'data_2018_RunB_v1' : tnpSample('data_2018_RunB' , eos2018Data_V3 + 'data/TnP_Prompt2018_RunB_v1_all.root' , lumi = 16.59 ),



#}
