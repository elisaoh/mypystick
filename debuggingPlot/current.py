import numpy as np

class currentState(object):
    """
    record current state for formants smoothing
    """
    def __init__(self,num=100,fp=[350,1500,2500],rms=400**2):
        self.num = num
        self.f1 = np.zeros(num) # current formants
        self.f2 = np.zeros(num) # current formants
        self.f3 = np.zeros(num) # current formants
        # initialize formants (previous formants)
        self.f1[num-1] = fp[0]
        self.f2[num - 1] = fp[1]
        self.f3[num - 1] = fp[2]
        self.fp = fp # previous formants

        self.rms = np.zeros(num) # currrent rms of signal
        self.rms[num-1] = rms

    def formants_add(self,formants,rms):
        # add current formants to tape
        frame = 1
        self.f1[:-frame] = self.f1[frame:]
        self.f1[-frame:] = formants[0]

        self.f2[:-frame] = self.f2[frame:]
        self.f2[-frame:] = formants[1]

        self.f3[:-frame] = self.f3[frame:]
        self.f3[-frame:] = formants[2]

        self.rms[:-frame] = self.rms[frame:]
        self.rms[-frame:] = rms


    def formants_cost(self,formants):
        # works
        M = np.zeros((len(formants),3))
        tran = 1  # weights for transition cost
        rang = 10**4  # weights for out of range
        for c in range(len(formants)):
            for f in range(3):
                M[c,f] = tran*(formants[c]-self.fp[f])**2

        f_min = [100,500,1000]
        f_max = [1500,3500,4500]
        for f in range(3):
            for c in range(len(formants)):
                M[formants[c] <= f_min[f], f] = rang
                M[formants[c] >= f_max[f], f] = rang
        return M

    def formants_pick(self,formants):
        # works
        M = self.formants_cost(formants)
        thold = 20000

        Big = 10**7
        f_now = np.zeros(3)

        # slow?
        cost_min = M.min()
        idx = np.unravel_index(np.argmin(M), (M.shape))
        if cost_min < thold:
            f_now[idx[1]] = formants[idx[0]]
        else:
            f_now[idx[1]] = self.fp[idx[1]]

        M[idx[0], :] = Big
        M[:, idx[1]] = Big
        cost_min = M.min()
        idx = np.unravel_index(np.argmin(M), (M.shape))
        if cost_min < thold:
            f_now[idx[1]] = formants[idx[0]]
        else:
            f_now[idx[1]] = self.fp[idx[1]]

        M[idx[0], :] = Big
        M[:, idx[1]] = Big
        cost_min = M.min()
        idx = np.unravel_index(np.argmin(M), (M.shape))
        if cost_min < thold:
            f_now[idx[1]] = formants[idx[0]]
        else:
            f_now[idx[1]] = self.fp[idx[1]]
        #
        return f_now

    def formants_smooth(self,formants,rms):
        fn = self.formants_pick(formants)
        self.formants_add(fn, rms)
        fs = np.zeros(3)

        weights = np.ones(self.num) # some weights for rms, 3 as num = 3 for now
        wr = np.multiply(weights,self.rms) # weighted rms
        rms_sum = np.sum(wr)

        fs[0] = np.dot(wr,self.f1)/rms_sum
        fs[1] = np.dot(wr,self.f2)/rms_sum
        fs[2] = np.dot(wr,self.f3)/rms_sum

        return fs













