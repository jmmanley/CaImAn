#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Wed Sep 20 17:52:23 2017
Basic demo for the OnACID algorithm using CNMF initialization. For a more
complete demo check the script demo_OnACID_mesoscope.py

@author: jfriedrich & epnev
"""

import os
import numpy as np
import pylab as pl
import caiman as cm
from caiman.source_extraction import cnmf as cnmf
from caiman.utils.visualization import view_patches_bar, plot_contours
from copy import deepcopy
from scipy.special import log_ndtr
from caiman.paths import caiman_datadir

#%%
def main():
    pass # For compatibility between running under Spyder and the CLI

#%% load data

    fname = [os.path.join(caiman_datadir(), 'example_movies', 'demoMovie.tif')]
    
# %% set up some parameters

    fr = 10  # frame rate (Hz)
    decay_time = 0.5  # approximate length of transient event in seconds
    gSig = [6, 6]  # expected half size of neurons
    p = 1  # order of AR indicator dynamics
    min_SNR = 3.5  # minimum SNR for accepting new components
    rval_thr = 0.90  # correlation threshold for new component inclusion
    gnb = 2  # number of background components

    # set up CNMF initialization parameters

    merge_thresh = 0.8  # merging threshold
    init_batch = 400  # number of frames for initialization
    patch_size = 32  # size of patch
    stride = 3  # amount of overlap between patches
    K = 4  # max number of components in each patch

#    opts = cnmf.params.CNMFParams()
#    opts.set('data', {'fnames': fname,
#                      'fr': fr,
#                      'decay_time': decay_time})
#    opts.set('patch', {'nb': gnb,
#                       'rf': patch_size//2,
#                       'stride': stride})
#    opts.set('online', {'min_SNR': min_SNR,
#                        'rval_thr': rval_thr,
#                        'init_batch': init_batch})
#    opts.set('init', {'gSig': gSig,
#                      'K': K,
#                      'nb': gnb})
#    opts.set('temporal', {'p': p})
#    opts.set('merging', {'thr': merge_thresh})
# %%
    params_dict = {'fr': fr,
                   'fnames': fname,
                   'decay_time': decay_time,
                   'gSig': gSig,
                   'p': p,
                   'min_SNR': min_SNR,
                   'rval_thr': rval_thr,
                   'nb': gnb,
                   'thr': merge_thresh,
                   'init_batch': init_batch,
                   'init_method': 'cnmf',
                   'rf': patch_size//2,
                   'stride': stride,
                   'normalize': False,
                   'K': K}
    opts = cnmf.params.CNMFParams(params_dict=params_dict)
#%% fit with online object
    cnm = cnmf.online_cnmf.OnACID(params=opts)
    cnm.dims = (60, 80)
    cnm.fit_online()

#%% plot contours
    
    print(('Number of components:' + str(cnm.estimates.A.shape[-1])))
    Cn = cm.load(fname[0], subindices=slice(0,500)).local_correlations(swap_dim=False)
    cnm.estimates.plot_contours(img=Cn)

##%% pass through the CNN classifier with a low threshold (keeps clearer neuron shapes and excludes processes)
#    use_CNN = True
#    if use_CNN:
#        # threshold for CNN classifier
#        thresh_cnn = 0.1
#        from caiman.components_evaluation import evaluate_components_CNN
#        predictions, final_crops = evaluate_components_CNN(
#            A, dims, gSig, model_name=os.path.join(caiman_datadir(), 'model', 'cnn_model'))
#        A_exclude, C_exclude = A[:, predictions[:, 1] <
#                                 thresh_cnn], C[predictions[:, 1] < thresh_cnn]
#        A, C = A[:, predictions[:, 1] >=
#                 thresh_cnn], C[predictions[:, 1] >= thresh_cnn]
#        noisyC = cnm.estimates.noisyC[gnb:cnm.M]
#        YrA = noisyC[predictions[:, 1] >= thresh_cnn] - C
#    else:
#        YrA = cnm.estimates.noisyC[gnb:cnm.M] - C

#%% plot results
    Y = cm.load(fname[0])
    cnm.estimates.view_components(Y.reshape((2000,4800), order='F').T)
    
#%%
# This is to mask the differences between running this demo in Spyder
# versus from the CLI
if __name__ == "__main__":
    main()
