from array import array
import ROOT

def setTDRStyle():
  tdrStyle =  ROOT.TStyle("tdrStyle","Style for P-TDR")

   #for the canvas:
  tdrStyle.SetCanvasBorderMode(0)
  tdrStyle.SetCanvasColor(ROOT.kWhite)
  tdrStyle.SetCanvasDefH(600) #Height of canvas
  tdrStyle.SetCanvasDefW(600) #Width of canvas
  tdrStyle.SetCanvasDefX(0)   #POsition on screen
  tdrStyle.SetCanvasDefY(0)


  tdrStyle.SetPadBorderMode(0)
  #tdrStyle.SetPadBorderSize(Width_t size = 1)
  tdrStyle.SetPadColor(ROOT.kWhite)
  tdrStyle.SetPadGridX(False)
  tdrStyle.SetPadGridY(False)
  tdrStyle.SetGridColor(0)
  tdrStyle.SetGridStyle(3)
  tdrStyle.SetGridWidth(1)

#For the frame:
  tdrStyle.SetFrameBorderMode(0)
  tdrStyle.SetFrameBorderSize(1)
  tdrStyle.SetFrameFillColor(0)
  tdrStyle.SetFrameFillStyle(0)
  tdrStyle.SetFrameLineColor(1)
  tdrStyle.SetFrameLineStyle(1)
  tdrStyle.SetFrameLineWidth(1)
  
#For the histo:
  #tdrStyle.SetHistFillColor(1)
  #tdrStyle.SetHistFillStyle(0)
  tdrStyle.SetHistLineColor(1)
  tdrStyle.SetHistLineStyle(0)
  tdrStyle.SetHistLineWidth(1)
  #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
  #tdrStyle.SetNumberContours(Int_t number = 20)

  tdrStyle.SetEndErrorSize(2)
  #tdrStyle.SetErrorMarker(20)
  #tdrStyle.SetErrorX(0.)
  
  tdrStyle.SetMarkerStyle(20)
  
#For the fit/function:
  tdrStyle.SetOptFit(1)
  tdrStyle.SetFitFormat("5.4g")
  tdrStyle.SetFuncColor(2)
  tdrStyle.SetFuncStyle(1)
  tdrStyle.SetFuncWidth(1)

#For the date:
  tdrStyle.SetOptDate(0)
  # tdrStyle.SetDateX(Float_t x = 0.01)
  # tdrStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
  tdrStyle.SetOptFile(0)
  tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
  tdrStyle.SetStatColor(ROOT.kWhite)
  tdrStyle.SetStatFont(42)
  tdrStyle.SetStatFontSize(0.025)
  tdrStyle.SetStatTextColor(1)
  tdrStyle.SetStatFormat("6.4g")
  tdrStyle.SetStatBorderSize(1)
  tdrStyle.SetStatH(0.1)
  tdrStyle.SetStatW(0.15)
  # tdrStyle.SetStatStyle(Style_t style = 1001)
  # tdrStyle.SetStatX(Float_t x = 0)
  # tdrStyle.SetStatY(Float_t y = 0)

# Margins:
  tdrStyle.SetPadTopMargin(0.05)
  tdrStyle.SetPadBottomMargin(0.13)
  tdrStyle.SetPadLeftMargin(0.16)
  tdrStyle.SetPadRightMargin(0.02)

# For the Global title:

  tdrStyle.SetOptTitle(0)
  tdrStyle.SetTitleFont(42)
  tdrStyle.SetTitleColor(1)
  tdrStyle.SetTitleTextColor(1)
  tdrStyle.SetTitleFillColor(10)
  tdrStyle.SetTitleFontSize(0.05)
  # tdrStyle.SetTitleH(0) # Set the height of the title box
  # tdrStyle.SetTitleW(0) # Set the width of the title box
  # tdrStyle.SetTitleX(0) # Set the position of the title box
  # tdrStyle.SetTitleY(0.985) # Set the position of the title box
  # tdrStyle.SetTitleStyle(Style_t style = 1001)
  # tdrStyle.SetTitleBorderSize(2)

# For the axis titles:

  tdrStyle.SetTitleColor(1, "XYZ")
  tdrStyle.SetTitleFont(42, "XYZ")
  tdrStyle.SetTitleSize(0.06, "XYZ")
  # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
  # tdrStyle.SetTitleYSize(Float_t size = 0.02)
  tdrStyle.SetTitleXOffset(0.9)
  tdrStyle.SetTitleYOffset(1.25)
  # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

# For the axis labels:

  tdrStyle.SetLabelColor(1, "XYZ")
  tdrStyle.SetLabelFont(42, "XYZ")
  tdrStyle.SetLabelOffset(0.007, "XYZ")
  tdrStyle.SetLabelSize(0.03, "XYZ")

# For the axis:

  tdrStyle.SetAxisColor(1, "XYZ")
  tdrStyle.SetStripDecimals(True)
  tdrStyle.SetTickLength(0.03, "XYZ")
  tdrStyle.SetNdivisions(510, "XYZ")
  tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
  tdrStyle.SetPadTickY(1)

# Change for log plots:
  tdrStyle.SetOptLogx(0)
  tdrStyle.SetOptLogy(0)
  tdrStyle.SetOptLogz(0)

  tdrStyle.cd()


def getEnvelopeHistograms(nominal, variations):
    """
    Compute envelop histograms create by all variations histograms. The envelop is simply the maximum
    and minimum deviations from nominal for each bin of the distribution
    Arguments:
    nominal: The nominal histogram
    variations: a list of histograms to compute the envelop from
    """

    if len(variations) < 2:
        raise TypeError("At least two variations histograms must be provided")
    
    # Use GetNcells() so that it works also for 2D histograms
    n_bins = nominal.GetNcells()
    for v in variations:
        if v.GetNcells() != n_bins:
            raise RuntimeError("Variation histograms do not have the same binning as the nominal histogram")

    up = nominal.Clone()
    up.SetDirectory(ROOT.nullptr)
    up.Reset()

    down = nominal.Clone()
    down.SetDirectory(ROOT.nullptr)
    down.Reset()

    for i in range(0, n_bins):
        minimum = float("inf")
        maximum = float("-inf")

        for v in variations:
            c = v.GetBinContent(i)
            minimum = min(minimum, c)
            maximum = max(maximum, c)

        up.SetBinContent(i, maximum)
        down.SetBinContent(i, minimum)

    return (up, down)


def equaliseBins(hist, title='BLR bins'):
    """Change bin boundaries along X axis of hist to 1, 2, ..., nBins+1.
    Does not affect actual bin contents or errors.
    Return a cloned histogram, no side-effect on hist."""

    newHist = hist.Clone()
    newHist.SetDirectory(ROOT.nullptr)
    xAxis = newHist.GetXaxis()
    xAxis.SetTitle(title)
    nBins = xAxis.GetNbins()
    newBins = array('f', range(1, nBins+2))
    xAxis.Set(nBins, newBins)
    return newHist


def openFileAndGet(path, mode="read"):
    """Open ROOT file in a mode, check if open properly, and return TFile handle."""

    _tf = ROOT.TFile.Open(path, mode)
    if not _tf or not _tf.IsOpen():
        raise Exception("Could not open file {}".format(path))
    return _tf

def readRecursiveDirContent(content, currTDir):
    """Fill dictionary content with the directory structure of currTDir.
    Every object is read and put in content with their name as the key.
    Sub-folders will define sub-dictionaries in content with their name as the key.
    """

    if not currTDir.InheritsFrom("TDirectory") or not isinstance(content, dict):
        return

    # Retrieve the directory structure inside the ROOT file
    currPath = currTDir.GetPath().split(':')[-1].split('/')[-1]

    if currPath == '':
        # We are in the top-level directory
        thisContent = content
    else:
        thisContent = {}
        content[currPath] = thisContent

    listKeys = currTDir.GetListOfKeys()

    for key in listKeys:
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            print("Entering sub-directory {}".format(obj.GetPath()))
            readRecursiveDirContent(thisContent, obj)
        else:
            name = obj.GetName()
            thisContent[name] = obj
            obj.SetDirectory(0)

def writeRecursiveDirContent(content, currTDir):
    """Write the items in dictionary content to currTDir, respecting the sub-directory structure."""

    if not currTDir.IsWritable() or not isinstance(content, dict):
        return

    for key, obj in content.items():
        if isinstance(obj, dict):
            print("Creating new sub-directory {}".format(key))
            subDir = currTDir.mkdir(key)
            writeRecursiveDirContent(obj, subDir)
        elif isinstance(obj, ROOT.TObject):
            currTDir.WriteTObject(obj, key)
