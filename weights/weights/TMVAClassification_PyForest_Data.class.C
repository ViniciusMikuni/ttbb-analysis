// Class: ReadPyForest_Data
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : PyRandomForest::PyForest_Data
TMVA Release   : 4.2.1         [262657]
ROOT Release   : 6.12/04       [396292]
Creator        : viniciusmikuni
Date           : Sat Jan 27 14:49:02 2018
Host           : Darwin Viniciuss-MacBook-Pro.local 17.2.0 Darwin Kernel Version 17.2.0: Fri Sep 29 18:27:05 PDT 2017; root:xnu-4570.20.62~3/RELEASE_X86_64 x86_64
Dir            : /Users/viniciusmikuni/cernbox/CMS/ttbbAnalysis/KinFitter/test/MVA/BDT
Training events: 468820
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "N" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
NEstimators: "850" [Integer, optional (default=10). The number of trees in the forest.]
Criterion: "gini" [String, optional (default='gini')       The function to measure the quality of a split. Supported criteria are       'gini' for the Gini impurity and 'entropy' for the information gain.       Note: this parameter is tree-specific.]
MaxDepth: "6" [integer or None, optional (default=None)       The maximum depth of the tree. If None, then nodes are expanded until       all leaves are pure or until all leaves contain less than       min_samples_split samples.       Ignored if ``max_leaf_nodes`` is not None.]
MinSamplesLeaf: "1" [integer, optional (default=1)       The minimum number of samples in newly created leaves.  A split is       discarded if after the split, one of the leaves would contain less then       ``min_samples_leaf`` samples.]
MinWeightFractionLeaf: "0.000000e+00" [//float, optional (default=0.)       The minimum weighted fraction of the input samples required to be at a       leaf node.]
MaxFeatures: "'auto'" [The number of features to consider when looking for the best split]
Bootstrap: "True" [boolean, optional (default=True)       Whether bootstrap samples are used when building trees.]
# Default:
VerbosityLevel: "Default" [Verbosity level]
H: "False" [Print method-specific help message]
CreateMVAPdfs: "False" [Create PDFs for classifier outputs (signal and background)]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
Normalise: "False" [Normalise input variables]
D: "False" [Use-decorrelated-variables flag]
VarTransformType: "Signal" [Use signal or background events to derive for variable transformation (the transformation is applied on both types of, course)]
TxtWeightFilesOnly: "True" [If True: write all training results (weights) as text files (False: some are written in ROOT format)]
NbinsMVAPdf: "60" [Number of bins used for the PDFs of classifier outputs]
NsmoothMVAPdf: "2" [Number of smoothing iterations for classifier PDFs]
MinSamplesSplit: "2" [integer, optional (default=2)      The minimum number of samples required to split an internal node.]
MaxLeafNodes: "None" [int or None, optional (default=None)      Grow trees with ``max_leaf_nodes`` in best-first fashion.      Best nodes are defined as relative reduction in impurity.      If None then unlimited number of leaf nodes.      If not None then ``max_depth`` will be ignored.]
OoBScore: "False" [ bool Whether to use out-of-bag samples to estimate      the generalization error.]
NJobs: "1" [ integer, optional (default=1)       The number of jobs to run in parallel for both `fit` and `predict`.       If -1, then the number of jobs is set to the number of cores.]
RandomState: "None" [int, RandomState instance or None, optional (default=None)      If int, random_state is the seed used by the random number generator;      If RandomState instance, random_state is the random number generator;      If None, the random number generator is the RandomState instance used      by `np.random`.]
Verbose: "0" [int, optional (default=0)      Controls the verbosity of the tree building process.]
WarmStart: "False" [bool, optional (default=False)      When set to ``True``, reuse the solution of the previous call to fit      and add more estimators to the ensemble, otherwise, just fit a whole      new forest.]
ClassWeight: "None" [dict, list of dicts, "auto", "subsample" or None, optional      Weights associated with classes in the form ``{class_label: weight}``.      If not given, all classes are supposed to have weight one. For      multi-output problems, a list of dicts can be provided in the same      order as the columns of y.      The "auto" mode uses the values of y to automatically adjust      weights inversely proportional to class frequencies in the input data.      The "subsample" mode is the same as "auto" except that weights are      computed based on the bootstrap sample for every tree grown.      For multi-output, the weights of each column of y will be multiplied.      Note that these weights will be multiplied with sample_weight (passed      through the fit method) if sample_weight is specified.]
FilenameClassifier: "MVA_weights/weights/PyRFModel_PyForest_Data.PyData" [Store trained classifier in this file]
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 9
simple_chi2                   simple_chi2                   simple_chi2                   simple_chi2                                                     'F'    [0.002432764275,23.5126171112]
meanDeltaRbtag                meanDeltaRbtag                meanDeltaRbtag                meanDeltaRbtag                                                  'F'    [0.395938187838,5.43606996536]
BDT_Comb                      BDT_Comb                      BDT_Comb                      BDT_Comb                                                        'F'    [-0.996163249016,0.984774649143]
jet_CSV[0]                    jet_CSV_0_                    jet_CSV[0]                    jet_CSV[0]                                                      'F'    [-10,1]
jet_CSV[1]                    jet_CSV_1_                    jet_CSV[1]                    jet_CSV[1]                                                      'F'    [-10,1]
jet_QGL[2]                    jet_QGL_2_                    jet_QGL[2]                    jet_QGL[2]                                                      'F'    [-20,1]
jet_QGL[3]                    jet_QGL_3_                    jet_QGL[3]                    jet_QGL[3]                                                      'F'    [-20,1]
jet_QGL[4]                    jet_QGL_4_                    jet_QGL[4]                    jet_QGL[4]                                                      'F'    [-20,1]
jet_QGL[5]                    jet_QGL_5_                    jet_QGL[5]                    jet_QGL[5]                                                      'F'    [-20,1]
NSpec 0


============================================================================ */

#include <array>
#include <vector>
#include <cmath>
#include <string>
#include <iostream>

#ifndef IClassifierReader__def
#define IClassifierReader__def

class IClassifierReader {

 public:

   // constructor
   IClassifierReader() : fStatusIsClean( true ) {}
   virtual ~IClassifierReader() {}

   // return classifier response
   virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

   // returns classifier status
   bool IsStatusClean() const { return fStatusIsClean; }

 protected:

   bool fStatusIsClean;
};

#endif

class ReadPyForest_Data : public IClassifierReader {

 public:

   // constructor
   ReadPyForest_Data( std::vector<std::string>& theInputVars ) 
      : IClassifierReader(),
        fClassName( "ReadPyForest_Data" ),
        fNvars( 9 ),
        fIsNormalised( false )
   {      
      // the training input variables
      const char* inputVars[] = { "simple_chi2", "meanDeltaRbtag", "BDT_Comb", "jet_CSV[0]", "jet_CSV[1]", "jet_QGL[2]", "jet_QGL[3]", "jet_QGL[4]", "jet_QGL[5]" };

      // sanity checks
      if (theInputVars.size() <= 0) {
         std::cout << "Problem in class \"" << fClassName << "\": empty input vector" << std::endl;
         fStatusIsClean = false;
      }

      if (theInputVars.size() != fNvars) {
         std::cout << "Problem in class \"" << fClassName << "\": mismatch in number of input values: "
                   << theInputVars.size() << " != " << fNvars << std::endl;
         fStatusIsClean = false;
      }

      // validate input variables
      for (size_t ivar = 0; ivar < theInputVars.size(); ivar++) {
         if (theInputVars[ivar] != inputVars[ivar]) {
            std::cout << "Problem in class \"" << fClassName << "\": mismatch in input variable names" << std::endl
                      << " for variable [" << ivar << "]: " << theInputVars[ivar].c_str() << " != " << inputVars[ivar] << std::endl;
            fStatusIsClean = false;
         }
      }

      // initialize min and max vectors (for normalisation)
      fVmin[0] = -1;
      fVmax[0] = 1;
      fVmin[1] = -1;
      fVmax[1] = 1;
      fVmin[2] = -1;
      fVmax[2] = 0.99999988079071;
      fVmin[3] = -1;
      fVmax[3] = 1;
      fVmin[4] = -1;
      fVmax[4] = 1;
      fVmin[5] = -1;
      fVmax[5] = 1;
      fVmin[6] = -1;
      fVmax[6] = 1;
      fVmin[7] = -1;
      fVmax[7] = 1;
      fVmin[8] = -1;
      fVmax[8] = 1;

      // initialize input variable types
      fType[0] = 'F';
      fType[1] = 'F';
      fType[2] = 'F';
      fType[3] = 'F';
      fType[4] = 'F';
      fType[5] = 'F';
      fType[6] = 'F';
      fType[7] = 'F';
      fType[8] = 'F';

      // initialize constants
      Initialize();

      // initialize transformation
      InitTransform();
   }

   // destructor
   virtual ~ReadPyForest_Data() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the 
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const;

 private:

   // method-specific destructor
   void Clear();

   // input variable transformation

   double fMin_1[3][9];
   double fMax_1[3][9];
   void InitTransform_1();
   void Transform_1( std::vector<double> & iv, int sigOrBgd ) const;
   void InitTransform();
   void Transform( std::vector<double> & iv, int sigOrBgd ) const;

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   const bool fIsNormalised;
   bool IsNormalised() const { return fIsNormalised; }
   double fVmin[9];
   double fVmax[9];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[9];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)
   inline double ReadPyForest_Data::GetMvaValue( const std::vector<double>& inputValues ) const
   {
      // classifier response value
      double retval = 0;

      // classifier response, sanity check first
      if (!IsStatusClean()) {
         std::cout << "Problem in class \"" << fClassName << "\": cannot return classifier response"
                   << " because status is dirty" << std::endl;
         retval = 0;
      }
      else {
         if (IsNormalised()) {
            // normalise variables
            std::vector<double> iV;
            iV.reserve(inputValues.size());
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(NormVariable( *varIt, fVmin[ivar], fVmax[ivar] ));
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
         else {
            std::vector<double> iV;
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(*varIt);
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
      }

      return retval;
   }

//_______________________________________________________________________
inline void ReadPyForest_Data::InitTransform_1()
{
   // Normalization transformation, initialisation
   fMin_1[0][0] = 0.002432764275;
   fMax_1[0][0] = 23.5126152039;
   fMin_1[1][0] = 0.00378946308047;
   fMax_1[1][0] = 23.5126171112;
   fMin_1[2][0] = 0.002432764275;
   fMax_1[2][0] = 23.5126171112;
   fMin_1[0][1] = 0.395938187838;
   fMax_1[0][1] = 5.39402532578;
   fMin_1[1][1] = 0.396668493748;
   fMax_1[1][1] = 5.43606996536;
   fMin_1[2][1] = 0.395938187838;
   fMax_1[2][1] = 5.43606996536;
   fMin_1[0][2] = -0.996163249016;
   fMax_1[0][2] = 0.984774649143;
   fMin_1[1][2] = -0.996145427227;
   fMax_1[1][2] = 0.814270555973;
   fMin_1[2][2] = -0.996163249016;
   fMax_1[2][2] = 0.984774649143;
   fMin_1[0][3] = -10;
   fMax_1[0][3] = 1;
   fMin_1[1][3] = -10;
   fMax_1[1][3] = 0.999605774879;
   fMin_1[2][3] = -10;
   fMax_1[2][3] = 1;
   fMin_1[0][4] = -10;
   fMax_1[0][4] = 1;
   fMin_1[1][4] = -10;
   fMax_1[1][4] = 0.999633967876;
   fMin_1[2][4] = -10;
   fMax_1[2][4] = 1;
   fMin_1[0][5] = -20;
   fMax_1[0][5] = 1;
   fMin_1[1][5] = -20;
   fMax_1[1][5] = 1;
   fMin_1[2][5] = -20;
   fMax_1[2][5] = 1;
   fMin_1[0][6] = -20;
   fMax_1[0][6] = 1;
   fMin_1[1][6] = -20;
   fMax_1[1][6] = 1;
   fMin_1[2][6] = -20;
   fMax_1[2][6] = 1;
   fMin_1[0][7] = -20;
   fMax_1[0][7] = 1;
   fMin_1[1][7] = -1;
   fMax_1[1][7] = 1;
   fMin_1[2][7] = -20;
   fMax_1[2][7] = 1;
   fMin_1[0][8] = -20;
   fMax_1[0][8] = 1;
   fMin_1[1][8] = -20;
   fMax_1[1][8] = 1;
   fMin_1[2][8] = -20;
   fMax_1[2][8] = 1;
}

//_______________________________________________________________________
inline void ReadPyForest_Data::Transform_1( std::vector<double>& iv, int cls) const
{
   // Normalization transformation
   if (cls < 0 || cls > 2) {
   if (2 > 1 ) cls = 2;
      else cls = 2;
   }
   const int nVar = 9;

   // get indices of used variables

   // define the indices of the variables which are transformed by this transformation
   static std::vector<int> indicesGet;
   static std::vector<int> indicesPut;

   if ( indicesGet.empty() ) { 
      indicesGet.reserve(fNvars);
      indicesGet.push_back( 0);
      indicesGet.push_back( 1);
      indicesGet.push_back( 2);
      indicesGet.push_back( 3);
      indicesGet.push_back( 4);
      indicesGet.push_back( 5);
      indicesGet.push_back( 6);
      indicesGet.push_back( 7);
      indicesGet.push_back( 8);
   } 
   if ( indicesPut.empty() ) { 
      indicesPut.reserve(fNvars);
      indicesPut.push_back( 0);
      indicesPut.push_back( 1);
      indicesPut.push_back( 2);
      indicesPut.push_back( 3);
      indicesPut.push_back( 4);
      indicesPut.push_back( 5);
      indicesPut.push_back( 6);
      indicesPut.push_back( 7);
      indicesPut.push_back( 8);
   } 

   static std::vector<double> dv;
   dv.resize(nVar);
   for (int ivar=0; ivar<nVar; ivar++) dv[ivar] = iv[indicesGet.at(ivar)];
   for (int ivar=0;ivar<9;ivar++) {
      double offset = fMin_1[cls][ivar];
      double scale  = 1.0/(fMax_1[cls][ivar]-fMin_1[cls][ivar]);
      iv[indicesPut.at(ivar)] = (dv[ivar]-offset)*scale * 2 - 1;
   }
}

//_______________________________________________________________________
inline void ReadPyForest_Data::InitTransform()
{
   InitTransform_1();
}

//_______________________________________________________________________
inline void ReadPyForest_Data::Transform( std::vector<double>& iv, int sigOrBgd ) const
{
   Transform_1( iv, sigOrBgd );
}
