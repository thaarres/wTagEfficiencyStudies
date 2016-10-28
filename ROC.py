from ROOT import *
import math
import time
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#762a83','#762a83','#de77ae','#de77ae','#de77ae','#a6dba0','#a6dba0','#a6dba0','#4393c3','#4393c3','#4393c3']
 colors = ['#762a83','#762a83','#de77ae','#de77ae','#a6dba0','#a6dba0','#4393c3','#4393c3']
 colors = ['#A43820','#A43820','#90AFC5','#90AFC5','#2A3132','#2A3132','#763626','#763626',]
 # colors = ['#762a83','#762a83','#762a83','#762a83','#de77ae','#de77ae','#de77ae','#de77ae','#a6dba0','#a6dba0','#a6dba0','#a6dba0','#4393c3','#4393c3','#4393c3','#4393c3']
 # colors = ['#762a83','#762a83','#de77ae','#de77ae','#a6dba0','#a6dba0','#4393c3','#4393c3']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]

def createGraph(denS,denB,hS,hB):
  wp = 0.45
  if hS.GetName().find("PUPPItau21")!=-1: wp = 0.40
  if hS.GetName().find("DDT")!=-1: wp = 0.52
  print "For inputfile %s using working point of %.2f" %(hS.GetName(),wp)
  nbins = hS.GetNbinsX()
  axis  = hS.GetXaxis()
  bmin  = axis.FindBin(0.)
  bmax  = axis.FindBin(1.)
  # denom_S = float( denS.Integral(0,100) )
  # denom_B = float( denB.Integral(0,100) )
  denom_S = float( denS.Integral(0,nbins) )
  denom_B = float( denB.Integral(0,nbins) )
  

  wpTau21 = TGraph(1)
  wpMass  = TGraph(1)
  g = TGraph(nbins)
  for i in range(nbins):
      # num_S = float( hS.Integral(nbins-i,nbins) ) #Cut from max bin to lower
      # num_B = float( hB.Integral(nbins-i,nbins) ) 
      
      num_S = float( hS.Integral(0,i) ) ##Cut from min bin to higher
      num_B = float( hB.Integral(0,i) )
      g.SetPoint( i, (num_S/denom_S), 1.-(num_B/denom_B) )     #eS vs. purity
      # g.SetPoint( i, (num_S/denom_S), ((num_B/denom_B) ) )   #eS vs. eB
      # g.SetPoint( i,(num_B/denom_B),(num_S/denom_S) )        #eB vs. eS
      
      if i == (wp+0.010)*100.:
        wpTau21.SetPoint(1, (num_S/denom_S), 1.-(num_B/denom_B) )
      if i == nbins-1:
        wpMass.SetPoint(1, (num_S/denom_S), 1.-(num_B/denom_B) )
      
  
  
  #-------To smoothen graph-----------
  # for i in range(1,40):
  #     num_S = float( hS.Integral(98-(i*5),98) )
  #     num_B = float( hB.Integral(98-(i*5),98) )
  #     # g.SetPoint( i+4,(num_S/denom_S), (1.-(num_B/denom_B)) )
  #     g.SetPoint( i+4,(num_S/denom_S), ((num_B/denom_B)) )
  #     # g.SetPoint(i+4,(num_B/denom_B),(num_S/denom_S) )
  # for i in range(1,6):
  #     num_S = float( hS.Integral(3,98) )
  #     num_B = float( hB.Integral(3,98) )
  #     # g.SetPoint(i+43,(num_S/denom_S), (1.-(num_B/denom_B)))
  #     g.SetPoint(i+43,(num_S/denom_S), ((num_B/denom_B)))
  #     # g.SetPoint(i+43,(num_B/denom_B),(num_S/denom_S) )
      
  # for i in range(5):
  #     num_S = float( hS.Integral(98-i,98) )
  #     num_B = float( hB.Integral(98-i,98) )
  #     # g.SetPoint( i, (num_S/denom_S), (1.-(num_B/denom_B) ) )
  #     g.SetPoint( i, (num_S/denom_S), ((num_B/denom_B) ) )
  #     # g.SetPoint( i,(num_B/denom_B),(num_S/denom_S) )
  #
  # for i in range(1,40):
  #     num_S = float( hS.Integral(98-(i*5),98) )
  #     num_B = float( hB.Integral(98-(i*5),98) )
  #     # g.SetPoint( i+4,(num_S/denom_S), (1.-(num_B/denom_B)) )
  #     g.SetPoint( i+4,(num_S/denom_S), ((num_B/denom_B)) )
  #     # g.SetPoint(i+4,(num_B/denom_B),(num_S/denom_S) )
  # for i in range(1,6):
  #     num_S = float( hS.Integral(3,98) )
  #     num_B = float( hB.Integral(3,98) )
  #   # g.SetPoint(i+43,(num_S/denom_S), (1.-(num_B/denom_B)))
  #     g.SetPoint(i+43,(num_S/denom_S), ((num_B/denom_B)))
  #   # g.SetPoint(i+43,(num_B/denom_B),(num_S/denom_S) )
  
  return g, wpMass,wpTau21 
   
def getPerformanceCurve(fFileS1, fFileB1):
  #get files and histograms
  file_S1 = TFile(fFileS1)
  file_B1 = TFile(fFileB1)
  
  print "Using signal file        = " ,file_S1.GetName()
  print "Using background file    = " ,file_B1.GetName()
  dens       = ["ForROC_Pruned_DEN","ForROC_PUPPI_DEN" ,"ForROC_PUPPI_DEN"]
  histonames = ["ForROC_tau21"     ,"ForROC_PUPPItau21","ForROC_DDT"]
  # bins =["_pt1","_pt2","_pt3","_pt4"]
  bins =["_pt1","_pt3"]
  histosS = []
  histosB =[]
  histosSden = []
  histosBden =[]
  
  for h in range(0,len(histonames)):
    for b in bins: 
      name = "%s%s"%(histonames[h],b)
      hS = TH1F( file_S1.Get(name) )
      hS.SetName(name+"_S")
      hB = TH1F(file_B1.Get(name))
      hB.SetName(name+"_B")   
      histosS.append(hS)
      histosB.append(hB)
      
      dname = "%s%s"%(dens[h],b)
      hSden = TH1F( file_S1.Get(dname) )
      hSden.SetName(dname+"_S")
      if h==2:
         hSden.SetName(dname+"_DDT_S")
      
      hBden = TH1F(file_B1.Get(dname))
      hBden.SetName(dname+"_B")
      if h==2:
         hBden.SetName(dname+"_DDT_B")

      histosSden.append(hSden)
      histosBden.append(hBden)
      
  mg      = [] 
  wpMass  = []
  wpTau21 = []
  for i in range (0,len(histosS)):
    print "Creating graph for: createGraph(%s,%s,%s,%s)" %(histosSden[i].GetName(),histosBden[i].GetName(),histosS[i].GetName(),histosB[i].GetName())
    graphs = createGraph(histosSden[i],histosBden[i],histosS[i],histosB[i])
    roc = graphs[0]
    roc.SetName(histosS[i].GetName())
    wpmass = graphs[1]
    wpmass.SetName(histosS[i].GetName())
    wptau21 = graphs[2]
    wptau21.SetName(histosS[i].GetName())
    print histosS[i].GetName()
    mg.append(roc)
    wpMass .append(wpmass)
    wpTau21.append(wptau21)
  return mg,wpMass, wpTau21

def formatGraph(graph, graphNum):
    palette = get_palette('gv')
    col = TColor()
    graphColor = col.GetColor(palette[graphNum])
    lineStyle = (graphNum % 2) +1
    graph.SetLineColor(graphColor)
    graph.SetMarkerColor(graphColor)
    graph.SetLineStyle(lineStyle)
    graph.SetLineWidth(4)

def plotPerformanceCurves(graphs, ordering,massWPs,tau21WPs, fTitle, fXAxisTitle, fYAxisTitle, fExtraInfo, fOutputFile, fXmin, fXmax, fYmin, fYmax, fLogy=0):

    # gROOT.SetBatch(kTRUE)

    c = TCanvas("c", "",800,800)
    c.cd()
    bkg = TH2D("bkg","",100,fXmin,fXmax,100,fYmin,fYmax)
    bkg.GetXaxis().SetTitle(fXAxisTitle)
    bkg.GetYaxis().SetTitle(fYAxisTitle)
    bkg.GetYaxis().SetNdivisions(507)
    bkg.GetXaxis().SetNdivisions(507)
    # bkg.SetTitleOffset(1.2,"X")
    # bkg.SetTitleOffset(1.5,"Y")
    bkg.Draw()
    # c.SetGridx()
 #    c.SetGridy()

    # legend = TLegend(.16,.74,.36,.93)
    # legend = TLegend(0.1834171,0.6204663,0.4183417,0.9002591)
    # legend = TLegend(0.41034171,0.6204663,0.8000183417,0.9002591)
    # legend = TLegend(0.4095477,0.6683938,0.798995,0.9002591) #for two per tagger
    legend = TLegend(0.1896985,0.1522021,0.3316583,0.4488342)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.0330)

    graphCounter = 0
    for g in range(0,len(graphs)):
      graph = graphs[g]
      print graph.GetName()
      print ordering[g]
      print "------"
      legend.AddEntry(graph, ordering[g],"l")
      formatGraph(graph,graphCounter)
      graph.Draw("L")
      
      
      formatGraph(massWPs[g] ,graphCounter)
      formatGraph(tau21WPs[g],graphCounter)
      
      massWPs[g].SetMarkerStyle(20)
      massWPs[g].SetMarkerSize(2.)
      massWPs[g].Draw("P")
      tau21WPs[g].SetMarkerStyle(23)
      tau21WPs[g].SetMarkerSize(2.)
      tau21WPs[g].Draw("P")
      graphCounter += 1
    
    gs = graphs[0].Clone()
    ms = massWPs[0].Clone()
    ts = tau21WPs[0].Clone()
    ms.SetMarkerStyle(20)
    ms.SetMarkerSize(2.)
    ts.SetMarkerStyle(23)
    ts.SetMarkerSize(2.)
    ms.SetMarkerColor(1)
    ts.SetMarkerColor(1)
    gs.SetLineColor(1)
    
    legend2 = TLegend(0.1896985,0.4733161,0.3630653,0.6670984)
    legend2.SetBorderSize(0)
    legend2.SetFillColor(0)
    legend2.SetFillStyle(0)
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.0330)
    legend2.SetHeader("65 GeV < M_{jet} < 105 GeV")
    legend2.AddEntry(ms,"M_{jet} selection only" ,"p")
    legend2.AddEntry(ts,"M_{jet} + #tau_{21} selection" ,"p")
    legend2.AddEntry(gs,"#tau_{21} scan" ,"l")
    
    
    if (fLogy):
        c.SetLogy()
    legend.Draw()
    legend2.Draw()
    addInfo = TPaveText(0.7072864,0.8044041,0.9974874,0.9209845,"NDC")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.030)
    addInfo.SetTextAlign(12)
    addInfo.AddText("<PU> = 12")
    addInfo.AddText("AK R = 0.8")
    addInfo.AddText(fExtraInfo)
    addInfo.Draw()
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    c.SaveAs(fOutputFile,"pdf")
    c.SaveAs(fOutputFile.replace(".pdf",".root"),"root")
    time.sleep(100)


def makePlots():


   ordering  = [] # vectors storing the order of legend entries
   mg        = [] # maps to hold legend entries and TGraph*s
   massWPs   = []
   tau21WPs  = []
   
   results = getPerformanceCurve("ExoDiBosonAnalysis.W_all.root","ExoDiBosonAnalysis.QCD_pTBinned_pythia8_76X.root")
   mg       = results[0]
   massWPs  = results[1]
   tau21WPs = results[2]
   
   # ordering.append("M_{Pruning}^{CHS}+#tau_{21}, ALL")
   ordering.append(" M_{Pruning}^{CHS} + #tau_{21}, p_{T} = 200 - 400 GeV")
   # ordering.append("M_{Pruning}^{CHS}+#tau_{21}, 400 GeV < p_{T} < 800 GeV")
   ordering.append(" M_{Pruning}^{CHS} + #tau_{21}, p_{T} = 800 - 1200 GeV")
   # ordering.append("M_{Pruning}^{CHS}+#tau_{21}, p_{T} > 1200 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +#tau_{21}, ALL")
   ordering.append(" M_{Softdrop}^{PUPPI} + #tau_{21}, p_{T} = 200 - 400 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +#tau_{21}, 400 GeV < p_{T} < 800 GeV")
   ordering.append(" M_{Softdrop}^{PUPPI} + #tau_{21}, p_{T} = 800 - 1200 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +#tau_{21}, p_{T} > 1200 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +DDT, ALL")
   ordering.append(" M_{Softdrop}^{PUPPI} + #tau_{21}^{DDT}, p_{T} = 200 - 400 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +#tau_{21}^{DDT}, 400 GeV < p_{T} < 800 GeV")
   ordering.append(" M_{Softdrop}^{PUPPI} + #tau_{21}^{DDT}, p_{T} = 800 - 1200 GeV")
   # ordering.append("M_{Softdrop}^{PUPPI} +#tau_{21}^{DDT}, p_{T} > 1200 GeV")

   # plotPerformanceCurves(mg,ordering,"","Tagging efficiency (W#rightarrowq#bar{q})","Mistagging rate (QCD)","|#eta| < 2.5, p_{T} > 200 GeV","roc_wtagging_vsEffB.pdf",0, 1, 0.0, 0.20)
   plotPerformanceCurves(mg,ordering,massWPs,tau21WPs,"","Tagging efficiency (W#rightarrowq#bar{q})","1 - Mistagging rate (QCD)","|#eta| < 2.5","roc_WqqvsQCD_2bins.pdf",0, 1, 0.85, 1.0)
   


if __name__ == "__main__":
    makePlots()
