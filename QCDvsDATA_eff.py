from ROOT import *
import time
import CMS_lumi, tdrstyle
import copy

tdrstyle.setTDRStyle()

CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 800; 
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


markerStyle = [20,24,23]

rebin = 2
path = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SamplesForWtagEfficiencies/"
filenames = ["ExoDiBosonAnalysis.QCD_pTBinned_pythia8_76X_mjj1200.root", "ExoDiBosonAnalysis.QCD_HTbinned_madgraph_76X_mjj1200.root","ExoDiBosonAnalysis.QCD_pTflat_herwig_76X_mjj1200.root"]

histos = ["numPT_mjtau21","numPT_mjtau21_puppi","numPT_mjDDT_puppi"]
dens   = ["denPT"        ,"denPT_puppi"        ,"denPT_puppi"]
color = [kGreen+3,kGreen-6,kGreen]
lineStyle = [1,3,8]


for filename in filenames:
  
  l = TLegend(0.3205312,0.5870035,0.5192288,0.8838515)
  
  filetmpMC = TFile.Open(path+filename,"READ")
  legend = ["QCD Pythia8, Pruning + #tau_{21}","QCD Pythia8, PUPPI SD + #tau_{21}","QCD Pythia8, PUPPI SD + DDT"]
  if filename.find("herwig") != -1:
    legend = ["QCD Herwig, Pruning + #tau_{21}","QCD Herwig, PUPPI SD + #tau_{21}","QCD Herwig, PUPPI SD + DDT"]
  if filename.find("madgraph") != -1:
    legend = ["QCD Pythia8+Madgraph, Pruning + #tau_{21}","QCD Pythia8+Madgraph, PUPPI SD + #tau_{21}","QCD Pythia8+Madgraph, PUPPI SD + DDT"]
       
  mg =  TMultiGraph()
  histolistMC = []
  histolistDATA = []
  
  l.SetTextSize(0.043)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  addInfo = TPaveText(0.6845965,0.3369315,0.9755922,0.5456246,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.038)
  addInfo.SetTextAlign(12)
  # addInfo.AddText("W-jet")
  addInfo.AddText("AK R=0.8")
  addInfo.AddText("M_{jj} > 1.2 TeV")
  addInfo.AddText("p_{T} > 200 GeV")
  addInfo.AddText("|#eta| #leq 2.4, |#Delta#eta_{jj}| #leq 1.3")
  i = -1 
  for h in histos:
    i +=1 
    x=[]
    y=[]
    denMC = TH1F(filetmpMC.Get(dens[i])).Rebin(rebin)
    numMC = TH1F(filetmpMC.Get(h)).Rebin(rebin)
    numMC.Divide(denMC)
    # g =  TGraphAsymmErrors()
    # g.Divide(num,den)
    # g.SetMarkerColor(color[i])
    # g.SetName("g%i"%i)
    numMC.SetLineColor(color[i])
    numMC.SetLineWidth(2)
    # g.SetMarkerSize(2)
    numMC.SetLineStyle(lineStyle[i])
    numMC.SetLineWidth(3)
    numMC.SetMarkerStyle(markerStyle[i])
    numMC.SetMarkerColor(color[i])
    numMC.SetMarkerSize(2)
    # mg.Add(g)
    histolistMC.append(numMC)
    l.AddEntry(numMC,"%s"%(legend[i]), "lp" )  

  filenameDATA = "ExoDiBosonAnalysis.Data_mjj1200.root"
  filetmp = TFile.Open(path+filenameDATA,"READ")

  legend = ["Data, Pruning + #tau_{21}","Data, PUPPI softdrop + #tau_{21}","Data, PUPPI softdrop + DDT"]

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
    # g.SetLineColor(color[i])
    # g.SetLineWidth(2)
    g.SetMarkerSize(2)
    g.SetMarkerStyle(markerStyle[i])
    mg.Add(g) 
    l.AddEntry(g,"%s"%(legend[i]), "p" )   
    num2 = copy.copy(num) 
    num2.Divide(den)
    histolistDATA.append(num2)  



  canv = TCanvas("c2","c2",W,H)
  canv.SetTickx()
  canv.SetTicky()  
  canv.GetWindowHeight()
  canv.GetWindowWidth()

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
  canv.SetFrameLineWidth(2)

  canv.SetTickx(0)
  canv.SetTicky(0)

  canv.Divide(1,2,0,0,0)
  canv.cd(1)

  p11_1 = canv.GetPad(1)
  p11_1.SetPad(0.01,0.26,0.99,0.98)
  p11_1.SetLeftMargin( L/W )
  p11_1.SetRightMargin( R/W )
  p11_1.SetTopMargin( T/H )
  p11_1.SetBottomMargin(0.032)

  vFrame = p11_1.DrawFrame(200,0.0,1800,0.10)  
  vFrame.SetTitle("")
  vFrame.SetXTitle("Jet p_{T}")
  vFrame.SetYTitle("Efficiency")
  vFrame.GetXaxis().SetTitleSize(0.00)
  vFrame.GetXaxis().SetTitleOffset(2.95)
  vFrame.GetXaxis().SetLabelOffset(2.95)
  vFrame.GetXaxis().SetLabelSize(0.00)
  
  vFrame.GetYaxis().SetTitleSize(0.06)
  vFrame.GetYaxis().SetTitleOffset(0.8)
  vFrame.GetYaxis().SetLabelSize(0.05)
  p11_1.SetFrameBorderMode(0)
  p11_1.SetFrameLineWidth(2)



  mg.Draw("Psame")
  for h in histolistMC:
      h.Draw("histSAME")
  p11_1.RedrawAxis()
  p11_1.Update()
  p11_1.GetFrame().Draw()
  CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)

  l.Draw("same")
  addInfo.Draw("same")
  mg.GetXaxis().SetLimits(200,1800)
  mg.SetMinimum(-0.0)
  mg.SetMaximum(0.08)
  mg.GetXaxis().SetTitleSize(0.00)
  mg.GetXaxis().SetTitleOffset(2.95)
  mg.GetXaxis().SetLabelOffset(2.95)
  mg.GetXaxis().SetLabelSize(0.00)
  mg.GetYaxis().SetTitle("Efficiency")
  mg.GetYaxis().SetNdivisions(204)
  mg.GetYaxis().SetTitleOffset(1.)


  canv.cd(2)
  p11_2 = canv.GetPad(2)
  p11_2.SetPad(0.01,0.02,0.99,0.27)
  p11_2.SetBottomMargin(0.35)
  p11_2.SetLeftMargin( L/W )
  p11_2.SetRightMargin( R/W )
  # p11_2.SetTopMargin( T/(H*2.5) )
  p11_2.SetGridx()
  p11_2.SetGridy()
  p11_2.SetFrameBorderMode(0)
  p11_2.SetFrameLineWidth(2)


  vFrame2 = p11_2.DrawFrame(200, 0.3, 1800, 1.7)
  vFrame2.SetTitle("")
  vFrame2.SetXTitle("Jet p_{T}")
  vFrame2.GetXaxis().SetTitleSize(0.06)
  vFrame2.SetYTitle("#frac{Data}{MC}")
  vFrame2.GetYaxis().CenterTitle()
  vFrame2.GetYaxis().SetTitleSize(0.16)
  vFrame2.GetYaxis().SetTitleOffset(0.3)
  vFrame2.GetYaxis().SetLabelSize(0.12)
  vFrame2.GetXaxis().SetTitleSize(0.18)
  vFrame2.GetXaxis().SetTitleOffset(0.90)
  vFrame2.GetXaxis().SetLabelSize(0.15)
  vFrame2.GetXaxis().SetNdivisions(204)
  
  rh1 = get_ratio(histolistDATA[0],histolistMC[0])
  rh1.Draw("Lsame")
  rh1.SetLineColor(color[0])
  rh1.SetMarkerColor(color[0])
  rh1.SetMarkerStyle(markerStyle[0])
  rh1.SetLineStyle(lineStyle[0])
  rh1.SetMarkerSize(2)
  rh2 = get_ratio(histolistDATA[1],histolistMC[1])
  rh2.Draw("Lsame")
  rh2.SetLineColor(color[1])
  rh2.SetMarkerColor(color[1])
  rh2.SetMarkerStyle(markerStyle[1])
  rh2.SetMarkerSize(2)
  rh2.SetLineStyle(lineStyle[1])
  rh3 = get_ratio(histolistDATA[2],histolistMC[2])
  rh3.Draw("Lsame")
  rh3.SetLineColor(color[2])
  rh3.SetMarkerColor(color[2])
  rh3.SetMarkerStyle(markerStyle[2])
  rh3.SetLineStyle(lineStyle[2])
  rh3.SetMarkerSize(2)
  li = get_line(200,1800,1,1)
  li.Draw()
  vFrame2.GetYaxis().SetNdivisions(005)
  p11_2.SetFrameBorderMode(0)
  p11_2.SetFrameLineWidth(2)
  
  p11_2.RedrawAxis()
  p11_1.RedrawAxis()
  canv.Update()
 

  cname = "BkgEff_DataMC_Pythia8_pT.pdf"
  if filename.find("herwig") != -1:
    cname = "BkgEff_DataMC_herwig_pT.pdf"
  if filename.find("madgraph") != -1:
    cname = "BkgEff_DataMC_Pythia8Madgraph_pT.pdf"  
  canv.SaveAs(cname)
  canv.SaveAs(cname.replace(".pdf",".root"))
  time.sleep(5)
