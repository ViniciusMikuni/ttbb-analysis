import numpy as np


import ROOT
import root_numpy

from sklearn import preprocessing, model_selection
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD
from keras.regularizers import l2


usevar1add = ['deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','deltaPhiaddb1','deltaPhiaddb2','deltaPhiaddw1','deltaPhiaddw2','deltaPhiaddtop1','deltaPhiaddtop2','deltaEtaaddb1','deltaEtaaddb2','deltaEtaaddw1','deltaEtaaddw2','deltaEtaaddtop1','deltaEtaaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','btagLR4b','btagLR3b','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','tt_pt','BDT_ttcc','BDT_ttlf','BDT_ttbb']
usevar2add = usevar1add + ['addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass']



# Load training dataset
filename = ROOT.TFile('..//Datasets/Correct_NoBtag_ttbar_full.root')

x_1ad = []
x_2ad = []
y_1ad = []
y_2ad = []
w_1ad = []
w_2ad = []
rfile = ROOT.TFile(filename, "READ")
classes = ['ttbb','ttcc','ttlf']

classes = {
    'ttcc':"ttCls<= 46 && ttCls > 0",
    'ttlf':"ttCls==0",
    'ttbb':"ttCls>=51"
}


for i_class, class_ in enumerate(classes):
    tree = rfile.Get('tree')
    x_class_1ad = np.zeros((tree.GetEntries(), len(usevar1add)))
    x_class_2ad = np.zeros((tree.GetEntries(), len(usevar2add)))
    x_conv_1ad = root_numpy.tree2array(tree, branches=usevar1add,selection='n_jets==7&&'+classes[class_])
    x_conv_2ad = root_numpy.tree2array(tree, branches=usevar2add,selection='n_jets>=8&&'classes[class_])
    for i_var, var in enumerate(usevar2add):
        x_class_2ad[:, i_var] = x_conv_2ad[var]
        x_2ad.append(x_class_2ad)
        if var in usevar1add:
            x_class_1ad[:, i_var] = x_conv_1ad[var]
            x_1ad.append(x_class_1ad)
            

    # Get weights
    w_class_1ad = np.zeros((tree.GetEntries(), 1))
    w_class_2ad = np.zeros((tree.GetEntries(), 1))
    w_conv_1ad = root_numpy.tree2array(
        tree, branches='weight',selection='n_jets==7&&'+classes[class_])
    w_conv_2ad = root_numpy.tree2array(
        tree, branches='weight',selection='n_jets>=8&&'classes[class_])
    w_class_1ad[:, 0] = w_conv_1ad['weight']
    w_class_2ad[:, 0] = w_conv_2ad['weight']
    w_1ad.append(w_class_1ad)
    w_2ad.append(w_class_2ad)

    # Get targets for this class
    y_class_1ad = np.zeros((tree.GetEntries(), len(classes)))
    y_class_2ad = np.zeros((tree.GetEntries(), len(classes)))
    y_class_1ad[:, i_class] = np.ones((tree.GetEntries()))
    y_class_2ad[:, i_class] = np.ones((tree.GetEntries()))
    y_1ad.append(y_class_1ad)
    y_2ad.append(y_class_2ad)

    # Stack inputs, targets and weights to a Keras-readable dataset
    x_1ad = np.vstack(x)  # inputs
    y_1ad = np.vstack(y)  # targets
    w_1ad = np.vstack(w)   # weights
    w_1ad = np.squeeze(w)  # needed to get weights into keras
    x_2ad = np.vstack(x)  # inputs
    y_2ad = np.vstack(y)  # targets
    w_2ad = np.vstack(w)   # weights
    w_2ad = np.squeeze(w)  # needed to get weights into keras


    # Split data in training and testing
    x_train_1ad, x_test_1ad, y_train_1ad, y_test_1ad, w_train_1ad, w_test_1ad = model_selection.train_test_split(
        x_1ad,
        y_1ad,
        w_1ad,
        test_size=0.25
    )
    x_train_2ad, x_test_2ad, y_train_2ad, y_test_2ad, w_train_2ad, w_test_2ad = model_selection.train_test_split(
        x_2ad,
        y_2ad,
        w_2ad,
        test_size=0.25
    )

    # Add callbacks

    path_model = os.path.join(config["output_path"],
                              "fold{}_keras_model.h5".format(args.fold))
    if "save_best_only" in config["model"]:
        if config["model"]["save_best_only"]:
            logger.info("Write best model to %s.", path_model)
            callbacks.append(
                ModelCheckpoint(path_model, save_best_only=True, verbose=1))

    if "reduce_lr_on_plateau" in config["model"]:
        logger.info("Reduce learning-rate after %s tries.",
                    config["model"]["reduce_lr_on_plateau"])
        callbacks.append(
            ReduceLROnPlateau(
                patience=config["model"]["reduce_lr_on_plateau"], verbose=1))

    # Train model
    if not hasattr(keras_models, config["model"]["name"]):
        logger.fatal("Model %s is not implemented.", config["model"]["name"])
        raise Exception
    logger.info("Train keras model %s.", config["model"]["name"])

    if config["model"]["batch_size"] < 0:
        batch_size = x_train.shape[0]
    else:
        batch_size = config["model"]["batch_size"]

    model_impl = getattr(keras_models, config["model"]["name"])
    model = model_impl(len(variables), len(classes))
    model.summary()
    model.fit(
        x_train,
        y_train,
        sample_weight=w_train,
        validation_data=(x_test, y_test, w_test),
        batch_size=batch_size,
        nb_epoch=config["model"]["epochs"],
        shuffle=True,
        callbacks=callbacks)

    # Save model
    if not "save_best_only" in config["model"]:
        logger.info("Write model to %s.", path_model)
        model.save(path_model)

B
