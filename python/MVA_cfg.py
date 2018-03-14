from os import environ
environ['KERAS_BACKEND'] = 'theano'
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
import ROOT
from keras.models import Sequential
from keras.layers import Dense, Activation, AlphaDropout,Conv1D,MaxPooling1D, Flatten, Reshape,Dropout,LSTM
from keras.optimizers import Adam, SGD, Nadam,Adadelta,RMSprop
from keras.regularizers import l2

batchs = 512
#nneurons = 64
def PyDNN_Opt(bkg, nvar,ncat = 2,activation = 'selu',nneurons=64,opt=Adam()):
    act = 'softmax' 
    lss = 'categorical_crossentropy' if ncat > 2 else 'binary_crossentropy'
    #opt = RMSprop(lr=1e-3)
    model = Sequential()


    # ####################################################################################
    # selu
    # ####################################################################################

    model.add(Dense(nneurons,input_dim = nvar,kernel_initializer='lecun_normal', activation='selu',bias_initializer='zeros'))
    model.add(AlphaDropout(0.1))
    model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    model.add(AlphaDropout(0.05))

    
    model.add(Dense(ncat, kernel_initializer='lecun_normal', bias_initializer='zeros', activation=act))
    ####################################################################################

    
    model.compile(loss=lss, optimizer=opt, metrics=['accuracy',])

    model.save('models/model'+bkg+'.h5')
    model.summary()



layoutString = "Layout=RELU|64,RELU|64,RELU|64,SOFTSIGN"
training0 =  "LearningRate=1e-3,Momentum=0.0,Repetitions=1,ConvergenceSteps=20,BatchSize=256,TestRepetitions=10,Regularization=L2,Multithreading=True,DropConfig=0.1,DropRepetitions=1"
#training1 = "LearningRate=1e-2,Momentum=0.0,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=7,Regularization=L2,Multithreading=True"

trainingStrategyString  = "TrainingStrategy=" 
trainingStrategyString += training0 
#trainingStrategyString += training0 + "|" + training1  

nnOptions = "!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=None:WeightInitialization=XAVIERUNIFORM"
nnOptions += ":" + layoutString + ":" +  trainingStrategyString + ":Architecture=CPU"

#"VarTransform=I,D,P",
methodList = {"BDT":[ROOT.TMVA.Types.kBDT,":".join(["!H","!V","NTrees=850","MaxDepth=6","BoostType=Grad","Shrinkage=0.1","UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts=30"])],
              "LH":[ROOT.TMVA.Types.kLikelihood,"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50"],
              "Cuts":[ROOT.TMVA.Types.kCuts,"H:!V:PopSize=600:Steps=50"],
              "MLP": [ROOT.TMVA.Types.kMLP, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator"],
              "SVM": [ROOT.TMVA.Types.kSVM,"Gamma=0.25:Tol=0.001:VarTransform=Norm"],
              "BDTA": [ROOT.TMVA.Types.kBDT, "!H:!V:NTrees=850:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.05:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=30"],
              "DNN": [ROOT.TMVA.Types.kDNN, nnOptions],
              "PyDNN":[ROOT.TMVA.Types.kPyKeras,":".join(["H","!V","NumEpochs=50","BatchSize="+str(batchs)])],
              "SVM" : [ROOT.TMVA.Types.kSVM, "VarTransform=Norm"],
              "Fish" : [ROOT.TMVA.Types.kFisher, "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" ],
              "FishG" : [ROOT.TMVA.Types.kFisher, "H:!V:Fisher:VarTransform=Gauss:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:Boost_Num=20:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.2:!Boost_DetailedMonitoring" ],
              
              "PDEFoam": [ROOT.TMVA.Types.kPDEFoam, "!H:!V::SigBgSeparate=F:MaxDepth=4:UseYesNoCell=T:DTLogic=MisClassificationError:FillFoamWithOrigWeights=F:TailCut=0:nActiveCells=500:nBin=20:Nmin=400:Compress=T"],
              "LH":[ROOT.TMVA.Types.kLikelihood,"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50:VarTransform=Decorrelate"],
              "PyGTB": [ROOT.TMVA.Types.kPyGTB,"!V:NEstimators=850"],
              "PyAda": [ROOT.TMVA.Types.kPyAdaBoost,"!V:NEstimators=1000"],
              "PyForest": [ROOT.TMVA.Types.kPyRandomForest, "!V:VarTransform=None:NEstimators=850:Criterion=gini:MaxFeatures=auto:MaxDepth=6:MinSamplesLeaf=1:NJobs=8:MinWeightFractionLeaf=0:Bootstrap=kTRUE"]}







# _DeltaR 5%bkg 20% sig
# qcd = '(meanDeltaRbtag < 1)'
# ttbar = '(meanDeltaRbtag > 2.0)'
# usevar = ['top1_m','top2_m','w1_m','w2_m','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','BDT_Comb','simple_chi2','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','BDT_QCD']

# _Diff 5% sig 40% sig
# qcd = "(BDT_QCD<-0.5)"
# ttbar = "(BDT_QCD>0.35)"
# usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']



# _Diff 7% sig 34% sig
# qcd = "(qgLR<0.3)"
# ttbar = "(qgLR>0.9)"
# usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']


# _Deep 5% sig 40% sig
# qcd = "(BDT_QCD<-0.5)"
# ttbar = "(BDT_QCD>0.35)"
# usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_DeepCSV[0]','jet_DeepCSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']



    # ####################################################################################
    # CNN Selu
    # ####################################################################################

    
    # model.add(Reshape((nvar,1), input_shape=(nvar,)))
    # model.add(Conv1D(nneurons, 3, activation='selu', input_shape=(None,nvar,1),kernel_initializer='lecun_normal', bias_initializer='zeros'))
    # model.add(MaxPooling1D(2))
    # model.add(AlphaDropout(0.1))
    # model.add(Flatten())

    # model.add(Dense(nneurons,kernel_initializer='lecun_normal', activation='selu',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    
    # model.add(Dense(ncat, kernel_initializer='lecun_normal', bias_initializer='zeros', activation=act))

    ####################################################################################



    
    # ####################################################################################
    # RNN Selu
    # ####################################################################################




    # model.add(Reshape((nvar,1), input_shape=(nvar,)))
    #model.add(LSTM(nneurons,input_shape=(None, nvar,1),kernel_initializer='lecun_normal', activation='selu',bias_initializer='zeros'))    # model.add(AlphaDropout(0.1))
    # model.add(Dense(nneurons,kernel_initializer='lecun_normal', activation='selu',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    
    # model.add(Dense(ncat, kernel_initializer='lecun_normal', bias_initializer='zeros', activation=act))

    ####################################################################################








    # ####################################################################################
    # CWoLa paper
    # ####################################################################################

    # model.add(Dense(nneurons, input_dim = nvar, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(nneurons, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(nneurons, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(ncat,  activation=act))



    # ####################################################################################
    # Selu
    # ####################################################################################
    # model.add(Dense(nneurons,input_dim = nvar,kernel_initializer='lecun_normal', activation='selu',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(nneurons, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    # model.add(AlphaDropout(0.2))
    # model.add(Dense(64, activation='selu',kernel_initializer='lecun_normal',bias_initializer='zeros'))
    
    # model.add(Dense(ncat, kernel_initializer='lecun_normal', bias_initializer='zeros', activation=act))

    ####################################################################################
