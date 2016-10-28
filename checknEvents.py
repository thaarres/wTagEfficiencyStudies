from ROOT import *


path = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SamplesForWtagEfficiencies/"
filenames = ["ExoDiBosonAnalysis.Data_mjj1200.root", "ExoDiBosonAnalysis.DATA_VV.root"]
filenames = ["ExoDiBosonAnalysis.Data_mjj1200.root","ExoDiBosonAnalysis.Data_mjj1200.root"]

nEV   = []
nFil  = []
nTrig = []
for ff in filenames:
  f = TFile.Open(path+ff,"READ")
  print ""
  print ff
  print "sumGenWeight    = ", (TH1F(f.Get("sumGenWeight"))).GetBinContent(1)
  print "nEvents_        = ", (TH1F(f.Get("nEvents"))).GetBinContent(1)
  print "nPassedJSON    = ", (TH1F(f.Get("nPassedJSON"))).GetBinContent(1)
  print "nPassedTrigger_ = ", (TH1F(f.Get("nPassedTrigger"))).GetBinContent(1)
  print "nPassedFilters_ = ", (TH1F(f.Get("nPassedFilter"))).GetBinContent(1)
  print ""
  print "numPT_mjtau21       = ", (TH1F(f.Get("numPT_mjtau21"      ))).GetEntries() 
  # print "numPT_mjtau21_puppi = ", (TH1F(f.Get("numPT_mjtau21_puppi"))).GetEntries()
  # print "numPT_mjDDT_puppi   = ", (TH1F(f.Get("numPT_mjDDT_puppi"  ))).GetEntries()
  print "denPT               = ", (TH1F(f.Get("denPT"              ))).GetEntries()
  # print "denPT_puppi         = ", (TH1F(f.Get("denPT_puppi"        ))).GetEntries()
  print "numPT_mjtau21/denPT = ", (TH1F(f.Get("numPT_mjtau21"      ))).GetEntries()  / (TH1F(f.Get("denPT"              ))).GetEntries() 
  print ""
  
  nEV  .append((TH1F(f.Get("nEvents"))).GetBinContent(1))
  nFil .append((TH1F(f.Get("nPassedFilter"))).GetBinContent(1))
  nTrig.append((TH1F(f.Get("nPassedTrigger"))).GetBinContent(1))
  

print ""
print "      DIFF (NEW MINUS OLD)     "
print "-------------------------------" 
print "nEvents_        = ", nEV  [0]-nEV  [1]
print "nPassedTrigger_ = ", nTrig[0]-nTrig[1]
print "nPassedFilters_ = ", nFil [0]-nFil [1]
print ""