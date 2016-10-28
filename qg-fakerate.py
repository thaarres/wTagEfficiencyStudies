from ROOT import *
import time
import CMS_lumi, tdrstyle
import copy

tdrstyle.setTDRStyle()

CMS_lumi.lumi_13TeV = "2.6 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def get_line(xmin,xmax,y,style):

   line = TLine(xmin,y,xmax,y)
   line.SetLineColor(kRed)
   line.SetLineStyle(style)
   line.SetLineWidth(2)
   return line
   
def get_ratio(hdata,histsum):
   ratio = TH1F("ratio","ratio",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         r = hdata.GetBinContent(b)/nbkg
         ratio.SetBinContent(b,r)
         err = r*TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b)/(ndata*ndata) + histsum.GetBinError(b)*histsum.GetBinError(b)/(nbkg*nbkg) )
         ratio.SetBinError(b,err)   
    
    
   ratio.SetLineWidth(3)
   # ratio.SetMarkerColor(kBlack)
   # ratio.SetMarkerStyle(20)
   # ratio.SetMarkerSize(1.)
   ratio.GetYaxis().SetTitle("#frac{Data}{MC}")
   # ratio.GetYaxis().SetNdivisions(504)
   ratio.GetYaxis().SetLabelSize(0.09)
   ratio.GetXaxis().SetLabelSize(0.12)
   ratio.GetYaxis().SetTitleSize(0.15)
   ratio.GetYaxis().SetTitleOffset(0.4)
   ratio.GetYaxis().CenterTitle()
   
   ratio.SetTitle("")
   ratio.SetXTitle("Jet p_{T}")
   ratio.GetXaxis().SetTitleSize(0.06)
   ratio.GetXaxis().SetTitleSize(0.15)
   ratio.GetXaxis().SetTitleOffset(0.90)
   return ratio

def get_palette(mode):

 palette = {}
 palette['gv'] = [] 
 
 colors = ["#99d8c9","#2ca25f","#fdbb84","#e34a33"]

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
 
palette = get_palette('gv')
col = TColor()

markerStyle = [20,20,26,26]

rebin = 2
path = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SamplesForWtagEfficiencies/"
filenames = ["ExoDiBosonAnalysis.QCD_pTBinned_pythia8_76X.root"]

histos = ["numPT_mjtau21_puppi_Q","numPT_mjtau21_puppi_G","numPT_mjDDT_puppi_Q","numPT_mjDDT_puppi_G"]
dens   = ["denPT_puppi_QG"       ,"denPT_puppi_QG"       ,"denPT_puppi_QG"     ,"denPT_puppi_QG"]
color = [kGreen+3,kGreen-6,kRed+3,kRed-6,]
lineStyle = [1,3,1,3]


for filename in filenames:
  
  filetmp1 = TFile.Open(path+filename,"READ")
  legend = ["q-jet, #tau_{21} #leq 0.4","g-jet, #tau_{21} #leq 0.4","q-jet, DDT #leq 0.52","g-jet, DDT #leq 0.52"]
       
  mg =  TMultiGraph()
  histolistMC = []
  histolistDATA = []
  
  l = TLegend(0.6168342,0.6398601,0.8634673,0.9073427)
  l.SetTextSize(0.04)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  addInfo = TPaveText(0.3548995,0.7282517,0.6451005,0.9195804,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.031)
  addInfo.SetTextAlign(12)
  addInfo.AddText("QCD Pythia8")
  addInfo.AddText("PUPPI AK R=0.8")
  addInfo.AddText("M_{jj} > 1.2 TeV")
  addInfo.AddText("65 GeV < M_{SD}<105 GeV")
  addInfo.AddText("p_{T} > 200 GeV, |#eta| < 2.5")
  i = -1 
  for h in histos:
    i +=1 
    x=[]
    y=[]
    den1 = TH1F(filetmp1.Get(dens[i])).Rebin(rebin)
    num1 = TH1F(filetmp1.Get(h)).Rebin(rebin)
    num1.Divide(den1)
    num1.SetLineColor(col.GetColor(palette[i]))
    num1.SetLineStyle(lineStyle[i])
    num1.SetLineWidth(3)
    num1.SetMarkerStyle(markerStyle[i])
    num1.SetMarkerColor(col.GetColor(palette[i]))
    num1.SetMarkerSize(2)
    num1.SetFillStyle(0)
    histolistMC.append(num1)
    l.AddEntry(num1,"%s"%(legend[i]), "l" )  

  histos = ["numPT_mjtau21_puppi","numPT_mjDDT_puppi"]
  dens   = ["denPT_puppi"        ,"denPT_puppi"]
  filenameDATA = "ExoDiBosonAnalysis.DATA_VV.root"
  filetmp = TFile.Open(path+filenameDATA,"READ")
  legend = ["Data, #tau_{21} #leq 0.4","Data, DDT #leq 0.52"]
  markerStyle = [20,26]

  i = -1 
  for h in histos:
    i +=1 
    x=[]
    y=[]
    den = TH1F(filetmp.Get(dens[i])).Rebin(rebin)
    num = TH1F(filetmp.Get(h)).Rebin(rebin)
    g =  TGraphAsymmErrors()
    g.Divide(num,den)
    g.SetName("g%i"%i)
    # g.SetLineColor(col.GetColor(palette[i]))
    # g.SetLineWidth(2)
    g.SetMarkerSize(2)
    g.SetMarkerStyle(markerStyle[i])
    mg.Add(g) 
    l.AddEntry(g,"%s"%(legend[i]), "pl" )   
    num2 = copy.copy(num) 
    num2.Divide(den)
    histolistDATA.append(num2)  


  # references for T, B, L, R
  T = 0.08*H_ref
  B = 0.12*H_ref 
  L = 0.12*W_ref
  R = 0.04*W_ref

  canv = TCanvas("c2","c2",50,50,W,H)
  canv.SetFillColor(0)
  canv.SetBorderMode(0)
  canv.SetFrameFillStyle(0)
  canv.SetFrameBorderMode(0)
  canv.SetLogy()
  canv.SetTickx(0)
  canv.SetTicky(0)
  canv.SetLeftMargin( L/W )
  canv.SetRightMargin( R/W )
  canv.SetTopMargin( T/H )
  canv.SetBottomMargin( B/H )

  mg.Draw("AP")
  mg.GetXaxis().SetLimits(200,2200)
  mg.SetMinimum(0.007)
  mg.SetMaximum(0.12)
  mg.GetYaxis().SetTitle("Efficiency")
  mg.GetXaxis().SetNdivisions(405)
  mg.GetYaxis().SetNdivisions(905)
  mg.GetXaxis().SetTitle("Jet p_{T}")
  mg.GetYaxis().SetTitleSize(0.06)
  mg.GetYaxis().SetTitleOffset(0.9)
  
  hs_tau21 = THStack("hs_tau21", "")
  hs_tau21.Add( histolistMC[0],"HIST")
  hs_tau21.Add( histolistMC[1],"HIST")
  hs_DDT = THStack("hs_DDT", "")
  hs_DDT.Add( histolistMC[2],"HIST")
  hs_DDT.Add( histolistMC[3],"HIST")
  
  
  hs_DDT.Draw("same")
  hs_tau21.Draw("same")
  histolistMC[2].Draw("HISTsame")
  # hs_DDT.Draw("histSAME")
  # mg.Add(g)

  CMS_lumi.CMS_lumi(canv, iPeriod, iPos)

  l.Draw("same")
  addInfo.Draw("same")
  canv.RedrawAxis()

  
  canv.Update()
  cname = "qgFakeRate_Pythia8_pT.pdf"
  canv.SaveAs(cname)
  canv.SaveAs(cname.replace(".pdf",".root"))
  time.sleep(200)
