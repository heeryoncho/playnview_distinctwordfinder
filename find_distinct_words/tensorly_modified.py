import numpy as np
import tensorly as tl
from tensorly.random import check_random_state
from tensorly.base import unfold
from tensorly.kruskal_tensor import kruskal_to_tensor
from tensorly.tenalg import khatri_rao

'''
BSD 3-Clause License

Copyright (c) 2016 The tensorly Developers.
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  c. Neither the name of the tensorly Developers  nor the names of
     its contributors may be used to endorse or promote products
     derived from this software without specific prior written
     permission. 


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

'''

'''

# Author: Jean Kossaifi <jean.kossaifi+tensors@gmail.com>
# Author: Chris Swierczewski <csw@amazon.com>
# Author: Sam Schneider <samjohnschneider@gmail.com>

# License: BSD 3 clause

*** This code was modified by the following person. ***

# Modified person info.: Heeryon Cho <heeryon.cho@gmail.com>
# Modified date: 2018/09/30 

# Modifications:

1. Fixed the weight of mode-3 values* by   


Japanese, Neutral, Korean words can be set using
'fixed_ja' & 'fixed_ko' variables.

'''


def initialize_factors(tensor, rank, random_state=None, non_negative=False):
    """Initialize factors used in `parafac`.

    Factor matrices are initialized using `random_state`.

    Parameters
    ----------
    tensor : ndarray
    rank : int
    random_state: int
        set to ensure reproducibility
    non_negative : bool, default is False
        if True, non-negative factors are returned

    Returns
    -------
    factors : ndarray list
        List of initialized factors of the CP decomposition where element `i`
        is of shape (tensor.shape[i], rank)

    """
    rng = check_random_state(random_state)

    factors = [tl.tensor(rng.random_sample((tensor.shape[i], rank)), **tl.context(tensor)) for i in
               range(tl.ndim(tensor))]
    if non_negative:
        return [tl.abs(f) for f in factors]
    else:
        return factors

    raise ValueError('Initialization method "{}" not recognized'.format(init))


def parafac(tensor, rank, n_iter_max=100, tol=1e-8,
            random_state=None, verbose=False, return_errors=False,
            mode_three_val=[[0.5, 0.5, 0.0],[0.0, 0.5, 0.5]]):
    """CANDECOMP/PARAFAC decomposition via alternating least squares (ALS)

    Computes a rank-`rank` decomposition of `tensor` [1]_ such that,

        ``tensor = [| factors[0], ..., factors[-1] |]``.

    Parameters
    ----------
    tensor : ndarray
    rank  : int
        Number of components.
    n_iter_max : int
        Maximum number of iteration
    tol : float, optional
        (Default: 1e-6) Relative reconstruction error tolerance. The
        algorithm is considered to have found the global minimum when the
        reconstruction error is less than `tol`.
    random_state : {None, int, np.random.RandomState}
    verbose : int, optional
        Level of verbosity
    return_errors : bool, optional
        Activate return of iteration errors


    Returns
    -------
    factors : ndarray list
        List of factors of the CP decomposition element `i` is of shape
        (tensor.shape[i], rank)
    errors : list
        A list of reconstruction errors at each iteration of the algorithms.

    References
    ----------
    .. [1] tl.G.Kolda and B.W.Bader, "Tensor Decompositions and Applications",
       SIAM REVIEW, vol. 51, n. 3, pp. 455-500, 2009.
    """

    factors = initialize_factors(tensor, rank, random_state=random_state)
    rec_errors = []
    norm_tensor = tl.norm(tensor, 2)

    # Mode-3 values that control the country factors are set using the
    # mode_three_val argument.

    fixed_ja = mode_three_val[0]
    fixed_ko = mode_three_val[1]

    for iteration in range(n_iter_max):
        for mode in range(tl.ndim(tensor)):
            pseudo_inverse = tl.tensor(np.ones((rank, rank)), **tl.context(tensor))

            factors[2][0] = fixed_ja   # set mode-3 values
            factors[2][1] = fixed_ko   # set mode-3 values

            for i, factor in enumerate(factors):
                if i != mode:
                    pseudo_inverse = pseudo_inverse*tl.dot(tl.transpose(factor), factor)
            factor = tl.dot(unfold(tensor, mode), khatri_rao(factors, skip_matrix=mode))
            factor = tl.transpose(tl.solve(tl.transpose(pseudo_inverse), tl.transpose(factor)))
            factors[mode] = factor

        if tol:
            rec_error = tl.norm(tensor - kruskal_to_tensor(factors), 2) / norm_tensor
            rec_errors.append(rec_error)

            if iteration > 1:
                if verbose:
                    print('reconstruction error={}, variation={}.'.format(
                        rec_errors[-1], rec_errors[-2] - rec_errors[-1]))

                if tol and abs(rec_errors[-2] - rec_errors[-1]) < tol:
                    if verbose:
                        print('converged in {} iterations.'.format(iteration))
                    break
                    
    if return_errors:
        return factors, rec_errors
    else:
        return factors
