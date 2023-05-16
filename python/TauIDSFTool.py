# Author: Izaak Neutelings (July 2019)
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
from __future__ import print_function
import os
from math import sqrt
import ctypes
if 'CMSSW_BASE' in os.environ: # assume CMSSW environment
  from TauPOG.TauIDSFs.helpers import ensureTFile, extractTH1, extractTF1DMandPT
  datapath = os.path.join(os.environ.get('CMSSW_BASE',""),"src/TauPOG/TauIDSFs/data")
else:
  from helpers import ensureTFile, extractTH1
  datapath = os.path.join(os.environ.get('TAUIDSFs',""),"data")
campaigns  = [
  '2016Legacy','2017ReReco','2018ReReco',
  'UL2016_preVFP', 'UL2016_postVFP', 'UL2017', 'UL2018',
]


class TauIDSFTool:
    
<<<<<<< HEAD
    def __init__(self, year, id, wp='Tight', dm=False, pTdm=False, emb=False,
=======
    def __init__(self, year, id, wp='Medium', wp_vsele='VVLoose', dm=False, ptdm=True, emb=False, highpT=False,
>>>>>>> 25ca8b42ae4171a2fb72a2a50e808afac8bb3f26
                 otherVSlepWP=False, path=datapath, verbose=False):
        """Choose the IDs and WPs for SFs. For available tau IDs and WPs, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau
        Options:
          dm:           use decay mode-dependent SFs
          emb:          use SFs for embedded samples
          otherVSlepWP: extra uncertainty if you are using a different DeepTauVSe/mu WP than used in the measurement
        """
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        self.ID       = id
        self.WP       = wp
        self.verbose  = verbose
        self.extraUnc = None
        self.filename = None
        
<<<<<<< HEAD
        if id in ['MVAoldDM2017v2','DeepTau2017v2p1VSjet', 'DeepTau2018v2p5VSjet']:
          if dm and pTdm==False : # DM-dependent SFs
=======
        if id in ['MVAoldDM2017v2','DeepTau2017v2p1VSjet']:
          if highpT: # pT-dependent SFs from W*->taunu events
            allowed_wp=['Loose','Medium','Tight','VTight']
            allowed_wp_vsele=['VVLoose','Tight']
            if id != 'DeepTau2017v2p1VSjet': raise IOError("Scale factors not available for ID '%s'!"%id)
            if wp not in allowed_wp or wp_vsele not in allowed_wp_vsele:
              raise IOError("Scale factors not available for this combination of WPs! Allowed WPs for VSjet are [%s]. Allowed WPs for VSele are [%s]"%(', '.join(allowed_wp),', '.join(allowed_wp_vsele)))
            if emb: raise IOError("Scale factors for embedded samples not available in this format! Use either pT-binned or DM-binned SFs.")
            fname = os.path.join(path,"TauID_SF_Highpt_%s_VSjet%s_VSele%s_Mar07.root" %(id, wp, wp_vsele))
            file = ensureTFile(fname,verbose=verbose)
            year_=year
            if year_.startswith('UL'): year_=year_[2:]
            self.func         = { }
            self.func[None]   = file.Get("DMinclusive_%s"%(year_))
            self.func['syst_alleras']   = file.Get("DMinclusive_%s_syst_alleras"%(year_))
            self.func['syst_oneera']   = file.Get("DMinclusive_%s_syst_%s"%(year_,year_))
            file.Close()
            fname_extrap = os.path.join(path,"TauID_SF_HighptExtrap_%s_Mar07.root" %(id))
            file_extrap = ensureTFile(fname_extrap,verbose=verbose)
            self.func['syst_extrap']   = file_extrap.Get("uncert_func_%sVSjet_%sVSe"%(wp,wp_vsele))
            file_extrap.Close()


          elif ptdm: # DM-dependent SFs with pT-dependence fitted
            self.DMs        = [0,1,10] if 'oldDM' in id else [0,1,10,11]
            allowed_wp=['Loose','Medium','Tight','VTight']
            allowed_wp_vsele=['VVLoose','Tight']
            if id != 'DeepTau2017v2p1VSjet': raise IOError("Scale factors not available for ID '%s'!"%id)
            if wp not in allowed_wp or wp_vsele not in allowed_wp_vsele:
              raise IOError("Scale factors not available for this combination of WPs! Allowed WPs for VSjet are [%s]. Allowed WPs for VSele are [%s]"%(', '.join(allowed_wp),', '.join(allowed_wp_vsele)))
            if emb: raise IOError("Scale factors for embedded samples not available in this format! Use either pT-binned or DM-binned SFs.")
            fname = os.path.join(path,"TauID_SF_dm_%s_VSjet%s_VSele%s_Mar07.root" %(id, wp, wp_vsele))
            file = ensureTFile(fname,verbose=verbose)
            year_=year
            if year_.startswith('UL'): year_=year_[2:]
            uncerts=['uncert0','uncert1','syst_alleras','syst_%s' % year_]

            self.funcs_dm0  = extractTF1DMandPT(file,'DM0_%s_fit' % year_,uncerts=uncerts+['syst_dm0_%s' % year_])
            self.funcs_dm1  = extractTF1DMandPT(file,'DM1_%s_fit' % year_,uncerts=uncerts+['syst_dm1_%s' % year_])
            self.funcs_dm10 = extractTF1DMandPT(file,'DM10_%s_fit' % year_,uncerts=uncerts+['syst_dm10_%s' % year_])
            self.funcs_dm11 = extractTF1DMandPT(file,'DM11_%s_fit' % year_,uncerts=uncerts+['syst_dm11_%s' % year_])

            self.getSFvsPT  = self.disabled
            self.getSFvsDM  = self.disabled
            self.getSFvsEta = self.disabled
          elif dm: # DM-dependent SFs
>>>>>>> 25ca8b42ae4171a2fb72a2a50e808afac8bb3f26
            if emb:
              if 'oldDM' in id:
                raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
              fname = os.path.join(path,"TauID_SF_dm_%s_%s_EMB.root"%(id,year))
            else:
              fname = os.path.join(path,"TauID_SF_dm_%s_%s.root"%(id,year))
            file = ensureTFile(fname,verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.filename   = fname
            self.DMs        = [0,1,10] if 'oldDM' in id else [0,1,10,11]
            self.getSFvsPT  = self.disabled
            self.getSFvsEta = self.disabled
            self.getSFvsPTDM = self.disabled
            if otherVSlepWP:
              if emb:
                self.extraUnc = 0.05
              else:
                self.extraUnc = 0.03

          #my addition
          elif pTdm and dm==False: #pT-dependent but divided in DMs
            fname = os.path.join(path,"TauID_SF_%s_%s.root"%(id,year))
            file = ensureTFile(fname,verbose=verbose)
            self.func         = { }
            dms = [0,1,10,11]
            for idm in dms: 
                self.func['Nom_DM'+str(idm)]   = file.Get("%s_DM%s_cent"%(wp,idm))
                self.func['Up_DM'+str(idm)]   = file.Get("%s_DM%s_up"%(wp,idm))
                self.func['Down_DM'+str(idm)] = file.Get("%s_DM%s_down"%(wp,idm))
            file.Close()
            self.filename   = fname
            self.getSFvsDM  = self.disabled
            self.getSFvsEta = self.disabled
            self.getSFvsPT  = self.disabled
          #################################


          else: # pT-dependent SFs
            if emb:
              if 'oldDM' in id:
                raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
              fname = os.path.join(path,"TauID_SF_pt_%s_%s_EMB.root"%(id,year))
            else:
              fname = os.path.join(path,"TauID_SF_pt_%s_%s.root"%(id,year))
            file = ensureTFile(fname,verbose=verbose)
            self.func         = { }
            self.func[None]   = file.Get("%s_cent"%(wp))
            self.func['Up']   = file.Get("%s_up"%(wp))
            self.func['Down'] = file.Get("%s_down"%(wp))
            file.Close()
            self.filename   = fname
            self.getSFvsDM  = self.disabled
            self.getSFvsEta = self.disabled
            self.getSFvsPTDM = self.disabled
            if otherVSlepWP:
              if emb:
                self.extraUnc = lambda pt: (0.05 if pt<100 else 0.15)
              else:
                self.extraUnc = lambda pt: (0.03 if pt<100 else 0.15)
        elif id in ['antiMu3','antiEleMVA6','DeepTau2017v2p1VSmu','DeepTau2017v2p1VSe']:
            if emb:
              raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
            fname = os.path.join(path,"TauID_SF_eta_%s_%s.root"%(id,year))
            file = ensureTFile(fname,verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.filename   = fname
            self.genmatches = [1,3] if any(s in id.lower() for s in ['ele','vse']) else [2,4]
            self.getSFvsPT  = self.disabled
            self.getSFvsDM  = self.disabled
            self.getSFvsPTDM = self.disabled
        else:
          raise IOError("Did not recognize tau ID '%s'!"%id)

    def getSFvsPTDM(self, idm, pt, genmatch=5, unc=None):
        """Get tau ID SF vs. tau pT divided in DMs"""
        if genmatch==5:
          if unc==None:
             return self.func["Nom_DM"+str(idm)].Eval(pt)
          else:
             return self.func[unc+"_DM"+str(idm)].Eval(pt)
        return 1.0

    
    def getSFvsPT(self, dm , pt, genmatch, unc=None):
        """Get tau ID SF vs. tau pT divided in DMs"""
        if genmatch==5:
          if self.extraUnc:
            sf       = self.func[None].Eval(pt)
            extraUnc = self.extraUnc(pt)
            errDown  = sqrt( (sf-self.func['Down'].Eval(pt))**2 + (sf*extraUnc)**2 )
            errUp    = sqrt( (sf-self.func['Up'  ].Eval(pt))**2 + (sf*extraUnc)**2 )
            if unc=='All':
              return sf-errDown, sf, sf+errUp
            elif unc=='Up':
              return sf+errUp
            elif unc=='Down':
              sfDown = (sf-errDown) if errDown<sf else 0.0 # prevent negative SF
              return sfDown
          else:
            if unc=='All':
              return self.func['Down'].Eval(pt), self.func[None].Eval(pt), self.func['Up'].Eval(pt)
          return self.func[unc].Eval(pt)
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0

    def getHighPTSFvsPT(self, pt, genmatch=5, unc=None):
        """Get High pT tau ID SF vs. tau pT."""
        if genmatch==5:
          x=ctypes.c_double(0.)
          y=ctypes.c_double(0.)
          # we only measured for 2 pT bins 100-200 and > 200 so return 1 of 2 values depending on whether pt is less than 200 or not
          self.func[None].GetPoint(0 if pt<200 else 1, x,y)
          sf=float(y.value)

          if not unc: return sf

          if 'stat_bin1' in unc and pt<200:
           # we define the stat error as the statistical error summed in quadrature with the systematic error that is uncorrelated by era
           # in principle these could be taken as seperate uncertainties but the effect of correlating the systematic part by pT bin will be negligible overall 
           if 'up' in unc:  sf+=sqrt(self.func[None].GetErrorY(0)**2 + self.func['syst_oneera'].GetErrorY(0)**2)
           if 'down' in unc:  sf-=sqrt(self.func[None].GetErrorY(0)**2 + self.func['syst_oneera'].GetErrorY(0)**2)
          if 'stat_bin2' in unc and pt>=200:
           # we define the stat error as the statistical error summed in quadrature with the systematic error that is uncorrelated by era
           # in principle these could be taken as seperate uncertainties but the effect of correlating the systematic part by pT bin will be negligible overall 
           if 'up' in unc:  sf+=sqrt(self.func[None].GetErrorY(1)**2 + self.func['syst_oneera'].GetErrorY(1)**2)
           if 'down' in unc:  sf-=sqrt(self.func[None].GetErrorY(1)**2 + self.func['syst_oneera'].GetErrorY(1)**2)
          if 'stat' in unc and 'bin' not in unc:
           # we define the stat error as the statistical error summed in quadrature with the systematic error that is uncorrelated by era
           # in principle these could be taken as seperate uncertainties but the effect of correlating the systematic part by pT bin will be negligible overall 
           if 'up' in unc:  sf+=sqrt(self.func[None].GetErrorY(0 if pt<200 else 1)**2 + self.func['syst_oneera'].GetErrorY(0 if pt<200 else 1)**2)
           if 'down' in unc:  sf-=sqrt(self.func[None].GetErrorY(0 if pt<200 else 1)**2 + self.func['syst_oneera'].GetErrorY(0 if pt<200 else 1)**2)
          if 'syst' in unc:
           if 'up' in unc:  sf+=self.func['syst_alleras'].GetErrorY(0 if pt<200 else 1)
           if 'down' in unc:  sf-=self.func['syst_alleras'].GetErrorY(0 if pt<200 else 1)
          if 'extrap' in unc:
            if 'up' in unc:  sf*=self.func['syst_extrap'].Eval(pt)
            if 'down' in unc:  sf*=(2.-self.func['syst_extrap'].Eval(pt))

          return sf
        return 1.0
    
    def getSFvsDM(self, pt, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau DM."""
        if genmatch==5 and dm in self.DMs and pt>40:
          bin = self.hist.GetXaxis().FindBin(dm)
          sf  = self.hist.GetBinContent(bin)
          err = self.hist.GetBinError(bin)
          if self.extraUnc:
            err = sqrt( err**2 + (sf*self.extraUnc)**2 )
          if unc=='Up':
            sf += err
          elif unc=='Down':
            sf = (sf-err) if err<sf else 0.0 # prevent negative SF
          elif unc=='All':
            sfDown = (sf-err) if err<sf else 0.0 # prevent negative SF
            return sfDown, sf, sf+err
          return sf
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
   
    def getSFvsDMandPT(self, pt, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau DM with pT dependence fitted"""
        if genmatch==5 and dm in self.DMs:

          # get correct functions depending on DM
          if dm==0: funcs = self.funcs_dm0
          elif 0<dm<=2: funcs = self.funcs_dm1
          elif dm==10: funcs = self.funcs_dm10
          elif dm==11: funcs = self.funcs_dm11
          
          if not unc: sf=funcs['nom'].Eval(max(min(pt,140.),20.))
          else: sf=funcs[unc].Eval(max(min(pt,140.),20.))
          return sf
        else:
          return 1.0
 
    def getSFvsEta(self, eta, genmatch, unc=None):
        """Get tau ID SF vs. tau eta."""
        eta = abs(eta)
        if genmatch in self.genmatches:
          bin = self.hist.GetXaxis().FindBin(eta)
          sf  = self.hist.GetBinContent(bin)
          err = self.hist.GetBinError(bin)
          if self.extraUnc:
            err = sqrt( err**2 + (sf*self.extraUnc)**2 )
          if unc=='Up':
            sf += err
          elif unc=='Down':
            sf = (sf-err) if err<sf else 0.0 # prevent negative SF
          elif unc=='All':
            sfDown = (sf-err) if err<sf else 0.0 # prevent negative SF
            return sfDown, sf, sf+err
          return sf
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    @staticmethod
    def disabled(*args,**kwargs):
        raise AttributeError("Disabled method.")
    

class TauESTool:
    def __init__(self, year, id='DeepTau2017v2p1VSjet', path=datapath, verbose=False):
        """Choose the IDs and WPs for SFs."""
        if "UL" in year:
          print(">>> TauESTool: Warning! Using pre-UL (%r) TESs at high pT (for uncertainties only)..."%(year))
          year_highpt = '2016Legacy' if '2016' in year else '2017ReReco' if '2017' in year else '2018ReReco'
        else:
          year_highpt = year
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        assert year_highpt in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year_highpt)
        fname_lowpt  = os.path.join(path,"TauES_dm_%s_%s.root"%(id,year))
        fname_highpt = os.path.join(path,"TauES_dm_%s_%s_ptgt100.root"%(id,year_highpt))
        file_lowpt   = ensureTFile(fname_lowpt, verbose=verbose)
        file_highpt  = ensureTFile(fname_highpt,verbose=verbose)
        self.hist_lowpt  = extractTH1(file_lowpt, 'tes')
        self.hist_highpt = extractTH1(file_highpt,'tes')
        self.hist_lowpt.SetDirectory(0)
        self.hist_highpt.SetDirectory(0)
        file_lowpt.Close()
        file_highpt.Close()
        self.pt_low  = 34  # average pT in Z -> tautau measurement (incl. in DM)
        self.pt_high = 170 # average pT in W* -> taunu measurement (incl. in DM)
        self.DMs     = [0,1,10] if "oldDM" in id else [0,1,10,11]
        self.filename = fname_lowpt
        self.filename_highpt = fname_highpt
    
    def getTES(self, pt, dm, genmatch=5, unc=None):
        """Get tau ES vs. tau DM."""
        if genmatch==5 and dm in self.DMs:
          bin = self.hist_lowpt.GetXaxis().FindBin(dm)
          tes = self.hist_lowpt.GetBinContent(bin)
          if unc!=None:
            if pt>=self.pt_high: # high pT
              bin_high = self.hist_highpt.GetXaxis().FindBin(dm)
              err      = self.hist_highpt.GetBinError(bin_high)
            elif pt>self.pt_low: # linearly interpolate between low and high pT
              bin_high = self.hist_highpt.GetXaxis().FindBin(dm)
              err_high = self.hist_highpt.GetBinError(bin_high)
              err_low  = self.hist_lowpt.GetBinError(bin)
              err      = err_low + (err_high-err_low)/(self.pt_high-self.pt_low)*(pt-self.pt_low)
            else: # low pT
              err      = self.hist_lowpt.GetBinError(bin)
            if unc=='Up':
              tes += err
            elif unc=='Down':
              tes = (tes-err) if err<tes else 0.0 # prevent negative TES
            elif unc=='All':
              tesDown = (tes-err) if err<tes else 0.0 # prevent negative TES
              return tesDown, tes, tes+err
          return tes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    def getTES_highpt(self, dm, genmatch=5, unc=None):
        """Get tau ES vs. tau DM for pt > 100 GeV"""
        if genmatch==5 and dm in self.DMs:
          bin = self.hist_highpt.GetXaxis().FindBin(dm)
          tes = self.hist_highpt.GetBinContent(bin)
          err = self.hist_highpt.GetBinError(bin)
          if unc=='Up':
            tes += err
          elif unc=='Down':
            tes = (tes-err) if err<tes else 0.0 # prevent negative TES
          elif unc=='All':
            tesDown = (tes-err) if err<tes else 0.0 # prevent negative TES
            return tesDown, tes, tes+err
          return tes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    

class TauFESTool:
    
    def __init__(self, year, id='DeepTau2017v2p1VSe', path=datapath, verbose=False):
        """Choose the IDs and WPs for SFs."""
        if "UL" in year:
          print(">>> TauFESTool: Warning! Using pre-UL (%r) energy scales for e -> tau fakes..."%(year))
          year = '2016Legacy' if '2016' in year else '2017ReReco' if '2017' in year else '2018ReReco'
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        fname = os.path.join(path,"TauFES_eta-dm_%s_%s.root"%(id,year))
        file  = ensureTFile(fname,verbose=verbose)
        graph = file.Get('fes')
        FESs  = { 'barrel':  { }, 'endcap': { } }
        DMs   = [0,1]
        i     = 0
        for region in ['barrel','endcap']:
          for dm in DMs:
            y    = graph.GetY()[i]
            yup  = graph.GetErrorYhigh(i)
            ylow = graph.GetErrorYlow(i)
            FESs[region][dm] = (max(0,y-ylow),y,y+yup) # prevent negative FES
            i += 1
        file.Close()
        self.filename   = fname
        self.FESs       = FESs
        self.DMs        = [0,1]
        self.genmatches = [1,3]
    
    def getFES(self, eta, dm, genmatch=1, unc=None):
        """Get electron -> tau FES vs. tau DM."""
        if dm in self.DMs and genmatch in self.genmatches:
          region = 'barrel' if abs(eta)<1.5 else 'endcap'
          fes    = self.FESs[region][dm]
          if unc=='Up':
            fes = fes[2]
          elif unc=='Down':
            fes = fes[0]
          elif unc!='All':
            fes = fes[1]
          return fes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
