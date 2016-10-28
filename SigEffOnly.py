from ROOT import *
import time
import CMS_lumi, tdrstyle


tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0

if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref
iPeriod = 0

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def get_palette(mode):

 palette = {}
 palette['gv'] = [] 
 # colors = ['#FF420E','#003B46','#80BD9E','#FF420E','#003B46','#80BD9E','#336B87','#763626','#003B46','#66A5AD']
 colors = ['#FF420E','#80BD9E','#FF420E','#80BD9E','#336B87','#336B87','#763626','#003B46','#66A5AD']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()
 

path = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SamplesForWtagEfficiencies/"
filename = "ExoDiBosonAnalysis.W_all.root"
filetmp = TFile.Open(path+filename,"READ")


legend = ["65 GeV < M_{Pruned}^{CHS} < 105 GeV","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV","65 GeV < M_{Pruned}^{CHS} < 105 GeV + #tau_{21} #leq 0.45","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV + #tau_{21} #leq 0.4","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV + #tau_{21}^{DDT} #leq 0.52"]
# legend = ["65 GeV < M_{Pruned}^{CHS} < 105 GeV","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV","65 GeV < M_{Pruned}^{PUPPI} < 105 GeV","65 GeV < M_{Pruned}^{CHS} < 105 GeV + #tau_{21} #leq 0.45","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV + #tau_{21} #leq 0.4","65 GeV < M_{Pruned}^{PUPPI} < 105 GeV + #tau_{21} #leq 0.4","65 GeV < M_{Softdrop}^{PUPPI} < 105 GeV + #tau_{21}^{DDT} #leq 0.52"]

# markerStyle = [20,22,24,26,32]
markerStyle = [24,26,20,22,23]



vars = ["PT","NPV"]

for var in vars:
  mg =  TMultiGraph()
  # histos = ["num%s_mj"%var,"num%s_mj_puppi"%var,"num%s_mj_puppi_pruning"%var,"num%s_mjtau21"%var,"num%s_mjtau21_puppi"%var,"num%s_mjtau21_puppi_pruning"%var,"num%s_mjDDT_puppi"%var]
  histos = ["num%s_mj"%var,"num%s_mj_puppi"%var,"num%s_mjtau21"%var,"num%s_mjtau21_puppi"%var,"num%s_mjDDT_puppi"%var]
  
  l = TLegend(0.1457286,0.6593264,0.3015075,0.9404145)
  l.SetTextSize(0.032)
  l.SetTextFont(42)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  if var.find("PT")!=-1: addInfo = TPaveText(0.1432161,0.1696891,0.4334171,0.2862694,"NDC")
  else: addInfo = TPaveText(0.1432161,0.1696891,0.4334171,0.2862694,"NDC")
  
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.030)
  addInfo.SetTextAlign(12)
  # addInfo.AddText("W-jet")
  addInfo.AddText("W-jet, AK R = 0.8")
  addInfo.AddText("p_{T} > 200 GeV")
  addInfo.AddText("|#eta| #leq 2.4 GeV")
  dname ="den%s"%var.upper()
  den  = TH1F(filetmp.Get(dname))
  # den = TH1F(filetmp.Get("denNPV"))
  i = -1 
  for h in histos:
  
    i +=1 
    x=[]
    y=[]
    num = TH1F(filetmp.Get(h))
    g =  TGraphAsymmErrors()
    g.Divide(num,den)
    g.SetMarkerColor(col.GetColor(palette[i]))
    g.SetName("g%i"%i)
    g.SetLineColor(col.GetColor(palette[i]))
    g.SetLineWidth(2)
    g.SetMarkerSize(2)
    g.SetMarkerStyle(markerStyle[i])
    mg.Add(g) 
    l.AddEntry(g,"%s"%(legend[i]), "p" )

  canvas = TCanvas("c2","c2",50,50,W,H)
  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)
  canvas.SetLeftMargin( L/W )
  canvas.SetRightMargin( R/W )
  # canvas.SetTopMargin( T/H )
  canvas.SetBottomMargin( B/H )
  canvas.SetTickx(0)
  canvas.SetTicky(0)
  
  mg.SetMinimum(0.0)
  mg.SetMaximum(1.45)
  mg.Draw("AP")
  mg.GetYaxis().SetTitleOffset(0.95)
  if var.find("PT")!=-1: mg.GetXaxis().SetTitle("Jet p_{T} (GeV)")
  else: mg.GetXaxis().SetTitle("Number of PVs")
  mg.GetYaxis().SetTitle("Efficiency")
  mg.GetYaxis().SetNdivisions(408)
  mg.GetXaxis().SetNdivisions(308)
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  SetOwnership( l, 1 )
  l.Draw()
  addInfo.Draw("same")
  cname = "WtagSigEffvs%s.pdf"%var
  canvas.SaveAs(cname)
  cname = "WtagSigEffvs%s.root"%var
  canvas.SaveAs(cname)
  time.sleep(5)
