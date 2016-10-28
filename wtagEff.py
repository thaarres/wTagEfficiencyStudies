from ROOT import *
import time
import CMS_lumi, tdrstyle


tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

W = 800
H = 800
H_ref = 700 
W_ref = 600 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

path = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SamplesForWtagEfficiencies/"
filenames = ["ExoDiBosonAnalysis.W_all.root","ExoDiBosonAnalysis.QCD_HTbinned_madgraph_76X.root"]

massVars = ['PUPPI','pruned']
# massVars = ['PUPPI']
#numPT_mjDDT_puppi,numNPV_mjDDT_puppi

for massVar in massVars:
  print massVar
  postfix = ''
  if massVar.find('PUPPI') !=-1: 
    postfix = '_puppi'
  
  print postfix
  
  mg_pT =  TMultiGraph()
  mg_nPV =  TMultiGraph()

  histos = ["numPT_mj%s"%postfix,"numPT_mjtau21%s"%postfix,"numNPV_mj%s"%postfix,"numNPV_mjtau21%s"%postfix]
  # histos = ["numPT_mj%s"%postfix,"numPT_mjDDT%s"%postfix,"numNPV_mj%s"%postfix,"numNPV_mjDDT%s"%postfix]
  print histos
  legend = ["W-jet, %s m_{j} selection"%massVar, "W-jet, %s m_{j} + #tau_{21} selection"%massVar, "QCD, %s m_{j} selection"%massVar, "QCD, %s m_{j} + #tau_{21} selection"%massVar]
  # legend = ["W-jet, %s m_{j} selection"%massVar, "W-jet, %s m_{j} + DDT selection"%massVar, "QCD, %s m_{j} selection"%massVar, "QCD, %s m_{j} + DDT selection"%massVar]
  color = [kGreen+3,kGreen-6,kGreen+3,kGreen-6,kGray+2,kGray+3,kGray+2,kGray+3]
  markerStyle = [20,24,20,24,23,32,23,32]

  l = TLegend(0.1683417,0.762228,0.3555276,0.9280311)
  l.SetTextSize(0.033)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)


  addInfo = TPaveText(0.7012563,0.8069948,0.991206,0.9235751,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.030)
  addInfo.SetTextAlign(12)

  if massVar.find('PUPPI') !=-1: addInfo.AddText("AK R=0.8 PUPPI")
  else: addInfo.AddText("AK R=0.8 CHS")
  addInfo.AddText("p_{T} > 200 GeV")
  addInfo.AddText("|#eta| < 2.4 GeV")

  k = -1
  for filename in filenames:
    filetmp = TFile.Open(path+filename,"READ")
    denPT  = TH1F(filetmp.Get("denPT"))
    denNPV = TH1F(filetmp.Get("denNPV"))
  
    i = -1 
    for h in histos:
      k +=1
      i +=1 
      x=[]
      y=[]
      den = denNPV
      num = TH1F(filetmp.Get(h))
      if i < 2:
        den = denPT
        num = TH1F(filetmp.Get(h))
      g =  TGraphAsymmErrors()
      g.Divide(num,den)
      g.SetMarkerColor(color[k])
      g.SetName("g%i"%i)
      g.SetLineColor(color[k])
      g.SetLineWidth(2)
      g.SetMarkerSize(2)
      g.SetMarkerStyle(markerStyle[k])
    
      if i < 2 :
        mg_pT.Add(g) 
        if k < 4: l.AddEntry(g,"%s"%(legend[i]), "p" )
        else: l.AddEntry(g,"%s"%(legend[i+2]), "p" )  
      else:
        mg_nPV.Add(g) 
      

  mgs = [mg_pT, mg_nPV]  
  title = ["Jet p_{T} (GeV)","Number of PVs"]
  outname = ["vpT","vnPVs"]

  ii = -1
  for mg in mgs:  
    ii += 1
    canvas = TCanvas("c%i"%ii,"c%i"%ii,W,H)
    # canvas.SetTickx()
    # canvas.SetTicky()
    # canvas.SetLogy()
    mg.SetMinimum(0.0)
    mg.SetMaximum(1.2)
    mg.Draw("AP")
    mg.GetXaxis().SetTitleSize(0.06)
    mg.GetXaxis().SetTitleOffset(0.95)
    mg.GetXaxis().SetLabelSize(0.05)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetLabelSize(0.05)
    mg.GetXaxis().SetTitle(title[ii])
    mg.GetYaxis().SetTitle("Efficiency")
    mg.GetYaxis().SetNdivisions(408)
    mg.GetXaxis().SetNdivisions(308)
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
    SetOwnership( l, 1 )
    l.Draw()
    addInfo.Draw("same")
    cname = "WtagSigEff_"+outname[ii]+"_"+massVar+".pdf"
    # cname = "WtagSigEff_"+outname[ii]+"_"+massVar+"_DDT.pdf"
    canvas.SaveAs(cname)
    cname = "WtagSigEff_"+outname[ii]+"_"+massVar+".root"
    # cname = "WtagSigEff_"+outname[ii]+"_"+massVar+"_DDT.root"
    canvas.SaveAs(cname)
    time.sleep(10)
