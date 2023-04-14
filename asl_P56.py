import numpy as np
from scipy.signal import lfilter


def asl_P56(x, fs, nbits=16):
    """
    This implements ITU P.56 method B for computing the active speech level.
    The input `x` is a speech signal with sampling frequency `fs`. The number of bits is `nbits`.(typically `16`)  
    """

    x = x[:]
    T = 0.23  # time constant of smoothing in seconds
    H = 0.2  # hangover time in seconds
    M = 15.9

    thres_no = nbits - 1  # number of thresholds

    I = np.ceil(fs*H)  # hangover time in samples
    g = np.exp(-1/(fs*T))  # smoothing factor
    c = np.zeros(int(thres_no))  # thresholds
    for i in range(-15, int(thres_no) - 15):
        c[i] = 2**i
    # vector with thresholds from one quantizing level up to half the maximum
    # code, at a step of 2, in the case of 16bit samples, from 2^-15 to 0.5;
    a = np.zeros(int(thres_no))  # activity counter for each level threshold
    # hangover counter for each level threshold
    hang = np.full(int(thres_no), I)

    sq = x.conj().T @ x  # long-term level square energy of x
    x_len = len(x)  # length of x

    x_abs = np.abs(x)
    p = lfilter([1-g], [1-g], x_abs)
    q = lfilter([1-g], [1-g], p)

    for k in range(x_len):
        for j in range(int(thres_no)):
            if (q[k] >= c[j]):
                a[j] = a[j] + 1
                hang[j] = 0
            elif hang[j] < I:
                a[j] = a[j] + 1
                hang[j] = hang[j] + 1
            else:
                break

    asl = 0
    asl_rms = 0
    if a[0] == 0:
        return
    else:
        AdB1 = 10*np.log10(sq/a[0] + 1e-10)

    CdB1 = 20*np.log10(c[0] + 1e-10)

    if AdB1 - CdB1 < M:
        return

    AdB = np.zeros(int(thres_no))
    CdB = np.zeros(int(thres_no))
    Delta = np.zeros(int(thres_no))

    AdB[0] = AdB1
    CdB[0] = CdB1
    Delta[0] = AdB1 - CdB1

    for j in range(1, int(thres_no)):
        AdB[j] = 10*np.log10(sq/(a[j]+1e-10)+1e-10)
        CdB[j] = 20*np.log10(c[j]+1e-10)


    #print(AdB)
    #print(CdB)
    for j in range(1, int(thres_no)):
        #print(a[j])
        if a[j] != 0:
            Delta[j] = AdB[j] - CdB[j]
            #print(Delta)
            if Delta[j] <= M:
                # interpolate to find the asl
                asl_ms_log, c10 = bin_interp(
                    AdB[j], AdB[j-1], CdB[j], CdB[j-1], M, 0.5)
                asl_ms = 10**(asl_ms_log/10)
                asl = (sq/x_len) / asl_ms
                c0 = 10**(c10/20)
                break
    return asl_ms, asl, c0


def bin_interp(upcount, lwcount, upthr, lwthr, Margin, tol):
    if tol < 0:
        tol = -tol

    # Check if extreme counts are not already the true active value
    iterno = 1
    if (np.abs(upcount-upthr - Margin) < tol):
        asl_ms_log = upcount
        cc = upthr
        return asl_ms_log, cc
    if (np.abs(lwcount-lwthr - Margin) < tol):
        asl_ms_log = lwcount
        cc = lwthr
        return asl_ms_log, cc

    # Initalize first middle for given (initial) bounds
    midcount = (upcount + lwcount)/2.0
    midthr = (upthr + lwthr)/2.0

    # Repeats loop until `diff' falls inside the tolerance (-tol<=diff<=tol
    while True:
        diff = midcount - midthr - Margin
        if np.abs(diff) <= tol:
            break
        # if tolerance is not met up to 20 iteractions, then relax the
        # tolerance by 10%
        iterno = iterno + 1

        if iterno > 20:
            tol = tol*1.1

        if diff > tol:  # then the new bounds are...
            midcount = (upcount+midcount)/2.0
            # upper and middle activitiy
            midthr = (upthr+midthr)/2.0
            # and the thresholds
        elif diff < -tol:  # then the new bounds are...
            midcount = (midcount+lwcount)/2.0
            # middle and lower activity
            midthr = (midthr+lwthr)/2.0
            # and the thresholds
    # Since the tolerance has been satisfied, midcount is selected
    # as the interpolated value with a tol [dB] tolerance.
    asl_ms_log = midcount
    cc = midthr
    return asl_ms_log, cc


if __name__ == '__main__':
    import soundfile as sf
    speech, fs = sf.read(
        '/media/george/stuff/VoiceBank/clean_testset_wav/p257_019.wav')
    print(asl_P56(speech, float(fs), float(16)))
    
    speech, fs = sf.read(
        '/media/george/stuff/VoiceBank/clean_testset_wav/p257_020.wav')
    print(asl_P56(speech, float(fs), float(16)))
