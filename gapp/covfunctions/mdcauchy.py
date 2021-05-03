"""
    GaPP: Gaussian Processes in Python
    Copyright (C) 2012, 2013  Marina Seikel
    University of Cape Town
    University of Western Cape
    marina [at] jorrit.de

    This file is part of GaPP.

    GaPP is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GaPP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""




import cov
import numpy as np
from numpy import array, exp, insert, reshape, sqrt, zeros
import warnings


class MultiDCauchy(cov.CovarianceFunction):
    # initialize class with initial hyperparameter theta
    def __init__(self, theta, X=None, Y=None):
        if (theta == None):
            # automatically provide initial theta if none is given
            sigmaf = (max(Y) - min(Y))/2.0
            l = array((np.max(X, axis=0) - np.min(X, axis=0))/2.0)
            theta = insert(l, 0, sigmaf)
        cov.CovarianceFunction.__init__(self, theta)
        if (np.min(self.theta) <= 0.0):
            warnings.warn("Illegal hyperparameters in the" + 
                          " initialization of MultiDCauchy.")

    # definition of the cauchy covariance function
    def covfunc(self):
        sigmaf = self.theta[0]
        l = self.theta[1:]
        xxl = np.sum(((self.x1 - self.x2)/l)**2)
        absl = float(sqrt(np.sum(l**2)))
        covariance = sigmaf**2/(absl * (1 + xxl))
        return covariance

    # gradient of the cauchy with respect to the hyperparameters
    # (d/dsigmaf,d/dl)k
    def gradcovfunc(self):
        sigmaf = self.theta[0]
        l = self.theta[1:]
        grad = zeros(len(self.theta))
        r = self.x1 - self.x2
        xxl = np.sum((r/l)**2)
        absl = float(sqrt(np.sum(l**2)))
        dk_dsigmaf = float(2 * sigmaf/(absl * (1 + xxl)))
        grad[0] = dk_dsigmaf
        grad[1:] = sigmaf**2/(absl * (1 + xxl))**2 * \
            (l[:]/absl * (1 + xxl) - 2. * absl * r[:]**2/l[:]**3) 
        return grad

    # derivative of the cauchy with respect to x2
    def dcovfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")

    # derivative of the cauchy with respect to x1 and x2
    # dk/(dx1 dx2)
    def ddcovfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")

    # second derivative of the cauchy with respect to x2
    def d2covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # second derivative of the cauchy with respect to x1 and x2
    # d^4k/(dx1^2 dx2^2)
    def d2d2covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # d^5/(dx1^2 dx2^3)
    def d2d3covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")

    # d^3k/(dx1 dx2^2)
    def dd2covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # d^3k/dx2^3
    def d3covfunc(self):
        if (self.multiD == 'True'): 
            raise RuntimeError("Derivative calculations are only implemented" + 
                               " for 1-dimensional inputs x.")


    # d^6k/dx1^3dx2^3
    def d3d3covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # d^4k/dx1dx2^3
    def dd3covfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # derivative of the gradient of the cauchy with respect to x2
    def dgradcovfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")


    # derivative of the gradient of the cauchy with 
    # respect to x1 and x2
    # dk/(d1 d2)
    def ddgradcovfunc(self):
        raise RuntimeError("Derivative calculations are only implemented" + 
                           " for 1-dimensional inputs x.")
