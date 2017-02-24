import os
import os.path as op
import numpy as np
from scipy.io.matlab import savemat
import shutil

import matplotlib.pyplot as plt
#matplotlib.use('svg')

from pyhrf.paradigm import restarize_events
from pyhrf.boldsynth.hrf import getCanoHRF
from pyhrf.tools import apply_to_leaves

def gen_spm_regs(subject_num):
<<<<<<< HEAD
    #HEROES
    nscans = 164
    tr = 2.5
    dt = .5
    #AINSI
    nscans = 291
    tr = 3.
    dt = tr #1.

    #HEROES
    paradigm_fn = './paradigm_data/paradigm_bilateral_v2_no_final_rest_nodelay.csv'  # motor
    paradigm_fn = './paradigm_data/paradigm_bilateral_v2_no_final_rest.csv'  # visual
    #AISNI
    paradigm_fn = './archives/paradigm_av.csv'
    #paradigm_fn = './archives/paradigm.csv'
    output_fn = './archives/'+subject_num+'/ASLf/regressors_ASLf.mat'
    
    #if not op.exists(op.dirname(output_fn)):
    #    raise Exception('Folders containing preprocessed data not found. '\
    #                    'Run Batch_HEROES_ASLf_2014.m with preprocs only before '
    #                    'launching this script')
=======
    nscans = 204
    tr = 2.5
    dt = .5

    paradigm_fn = './paradigm.csv'
    output_fn = './gin_struct/archives/'+subject_num+'/ASLf/regressors_ASLf.mat'
    
    if not op.exists(op.dirname(output_fn)):
        raise Exception('Folders containing preprocessed data not found. '\
                        'Run Batch_HEROES_ASLf_2014.m with preprocs only before '
                        'launching this script')
>>>>>>> salma1601/retreat

    if not op.exists(paradigm_fn):
        raise Exception('Paradigm file not found in current directory. '
                        'Should have been generated by another script')

<<<<<<< HEAD
    #HEROES
    #condition_order = ['checkerboard_motor_d2500_left', 'checkerboard_motor_d5000_left',
    #                   'checkerboard_motor_d2500_right', 'checkerboard_motor_d5000_right']
    condition_order = None # any order
=======
    condition_order = ['checkerboard_motor_d2000', 'checkerboard_motor_d4000',
                       'checkerboard_motor_d6000']
>>>>>>> salma1601/retreat
    build_matrix(paradigm_fn, output_fn, nscans, tr, dt,
                 cond_order=condition_order)
    

<<<<<<< HEAD
def build_matrix(paradigm_fn, output_fn, nscans, tr, dt, plot=True,
=======
def build_matrix(paradigm_fn, output_fn, nscans, tr, dt, plot=False,
>>>>>>> salma1601/retreat
                 save_dmat_png=False, cond_order=None):
    """
    cond_order is used to sort the column of the design matrix
    """
    onsets, dur = load_paradigm(paradigm_fn)
    #remove 'final_rest':
    onsets = dict( (n,o) for n,o in onsets.iteritems() if n != 'final_rest' )
    dur = dict( (n,o) for n,o in dur.iteritems() if n != 'final_rest' )

    print 'Onsets description:'
    print_descrip_onsets(onsets)

    tMax = tr * nscans

    #save_dmat_png = True
    #plot = True

<<<<<<< HEAD
    thc, hc = getCanoHRF(25, dt)
=======
    thc, hc = getCanoHRF(25, tr)
>>>>>>> salma1601/retreat
    dhc = np.diff(hc)
    ddhc = np.diff(dhc)
    nderivatives = 1

<<<<<<< HEAD
    plt.plot(hc)
    plt.show()
    
=======
>>>>>>> salma1601/retreat
    ons = onsets
    nbConditions = len(ons)
    #regressors: [nconds * nderiv] x [ASL,BOLD] + basal_perf + constant
    nregressors = (nbConditions * nderivatives) + 1
    x =  np.zeros((nscans, nregressors))
    convMode = 'full'
    #if convMode == 'same':
    #    xconv = zeros((nscans, nregressors))
    #else:
    #    xconv = zeros((nscans+len(hc)-1, nregressors))

    xconv = np.zeros((nscans, nregressors))
    reg_names = []
    j=0
    if cond_order is None:
        cond_order = ons.iterkeys()

    for i,cname in enumerate(cond_order):
        o = ons[cname]
        d = dur[cname]
        x[:,i] = restarize_events(o, d, tr, tMax)[:nscans]
        xconv[:,j] = np.convolve(x[:,i], hc*3., mode=convMode)[:len(x[:,i])]
        if nderivatives >= 2:
            xconv[:,j+1] = np.convolve(x[:,i], dhc*3., mode=convMode)[:len(x[:,i])]
        if nderivatives >= 3:
            xconv[:,j+2] = np.convolve(x[:,i], ddhc*3., mode=convMode)[:len(x[:,i])]
        j+=nderivatives
        reg_names.append(cname)
        #plt.plot(x[:,i])
        #plt.plot(xconv[:,i])
        #plt.show()
        #sys.exit(0)
    x[:,-1] = 1.
    xconv[:,-1] = 1. #max(hc)
    reg_names.append('baseline')
    vmax = max(x.max(),xconv.max())
    vmin = min(x.min(),xconv.min())

    tag_ctrl_weights = np.ones(nscans)
    tag_ctrl_weights[1::2] = -1
    xconv = np.hstack((xconv, xconv * tag_ctrl_weights[:,np.newaxis]))
    reg_names += map(lambda x: x+'_ASL', reg_names)
<<<<<<< HEAD
    #reg_names.append('perf_basale')

    ib = reg_names.index('baseline')
    xconv = xconv[:,range(0,ib)+range(ib+1,xconv.shape[1])]
    
    import pyhrf.vbjde.vem_tools as vt
    ndrift = 4
    drift = vt.PolyMat(nscans, ndrift, tr)
    xconv = np.append(xconv, drift, axis=1)
    for d in xrange(0, drift.shape[1]):
        reg_names.append('drift' + str(d))
    
    reg_names.pop(ib)
    to_save = {'r': xconv, 'reg_names': reg_names}
=======
    reg_names.append('perf_basale')

    ib = reg_names.index('baseline')
    xconv = xconv[:,range(0,ib)+range(ib+1,xconv.shape[1])]
    reg_names.pop(ib)
    to_save = {'r' : xconv,
               'reg_names' : reg_names}

>>>>>>> salma1601/retreat
    print 'Save regressors to:', output_fn
    savemat(output_fn, to_save)

    extent = (0, x.shape[1], x.shape[0]*tr, 0)
    if plot:
        n = plt.Normalize(vmin,vmax)
        plt.matshow(x, aspect='.15', cmap=plt.cm.gray_r, extent=extent)
        plt.title('onsets')

        #ax = plt.gca()
        #ax.set_axis_off()

    if save_dmat_png:
        fn = './design_matrix_onsets_only.png'
        plt.colorbar(shrink=.35)
        plt.savefig(fn, dpi=300)
        os.system('convert %s -trim %s' %(fn,fn))

    if plot:
        plt.matshow(xconv, aspect='.15', cmap=plt.cm.gray_r, extent=extent)
        plt.title('convolved onsets')
        #ax = plt.gca()
        #ax.set_axis_off()
<<<<<<< HEAD
        plt.show()
        
        plt.plot(x[:,:4])
        plt.plot(xconv[:,:4])
        plt.show()
=======

>>>>>>> salma1601/retreat

    if save_dmat_png:
        if nderivatives == 1:
            plt.colorbar(shrink=.35)
            fn = './design_matrix_convolved.png'
        elif nderivatives == 2:
            fn = './design_matrix_convolved_hrf_deriv.png'
        elif nderivatives == 3:
            cb = plt.colorbar(shrink=.12)
            for t in cb.ax.get_yticklabels():
                t.set_fontsize(10)
            fn = './design_matrix_convolved_hrf_deriv2.png'
        plt.savefig(fn, dpi=300)
        os.system('convert %s -trim %s' %(fn,fn))
    # else:
    #     plt.colorbar(shrink=.15)
    #     plt.show()



def load_paradigm(fn):
    from collections import defaultdict

    fn_content = open(fn).readlines()
    onsets = defaultdict(list)
    durations = defaultdict(list)
    for line in fn_content:
        sline = line.split(' ')
<<<<<<< HEAD
        print 'sline:', sline
        sess, cond, onset, duration = sline
        #if len(sline) < 4:
        #    cond, onset, _ = sline
        #else:
        #    sess, cond, onset, duration, amplitude = sline
=======
        #print 'sline:', sline
        if len(sline) < 4:
            cond, onset, _ = sline
        else:
            sess, cond, onset, duration, amplitude = sline
>>>>>>> salma1601/retreat
        onsets[cond.strip('"')].append(float(onset))
        durations[cond.strip('"')].append(float(duration))

    ons_to_return = {}
    dur_to_return = {}
    for cn, ons in onsets.iteritems():
        sorting = np.argsort(ons)
        ons_to_return[cn] = np.array(ons)[sorting]
        dur_to_return[cn] = np.array(durations[cn])[sorting]

    return ons_to_return, dur_to_return

def print_descrip_onsets(onsets):
    onsets = dict( (n,o) for n,o in onsets.iteritems() \
                       if n not in ['blanc','blank'] )
    all_onsets = np.hstack(onsets.values())
    diffs = np.diff(np.sort(all_onsets)) 
    #pprint(onsets)
    print 'mean ISI:', format_duration(diffs.mean())
    print 'max ISI:', format_duration(diffs.max())
    print 'min ISI:', format_duration(diffs.min())
    print 'first event:', format_duration(all_onsets.min())
    print 'last event:', format_duration(all_onsets.max())

def format_duration(dt):
    s = ''
    if dt/3600 >= 1:
        s += '%dH' %int(dt/3600)
        dt = dt%3600
    if dt/60 >= 1:
        s += '%dmin' %int(dt/60)
        dt = int(dt%60)
    s += '%1.3fsec' %dt
    return s

if __name__ == '__main__':
<<<<<<< HEAD
    subjects = ['AINSI_001_GC', 'AINSI_005_SB', 'AINSI_010_TV']
    for isubj, subject_num in enumerate(subjects):
        #subject_num = 'AINSI_005_SB'
        gen_spm_regs(subject_num)
=======
    main()
>>>>>>> salma1601/retreat