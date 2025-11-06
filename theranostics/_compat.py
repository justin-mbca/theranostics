"""Small runtime compatibility helpers used in local development runs.

This module applies minimal, well-documented shims so third-party libraries
that expect older/newer pandas/scipy APIs work in our local env. Prefer
pinning proper versions in `requirements.txt` for production; this shim
is a low-risk developer convenience.
"""
import numpy as np
import scipy.integrate as integrate
import pandas as pd

# Ensure trapz exists (some SciPy builds expose it differently)
integrate.trapz = getattr(integrate, "trapz", np.trapz)

# Accept and drop unexpected datetime kwarg in describe
from pandas import DataFrame
_orig_describe = DataFrame.describe

def _describe_compat(self, *args, **kwargs):
    kwargs.pop("datetime_is_numeric", None)
    return _orig_describe(self, *args, **kwargs)

DataFrame.describe = _describe_compat

# Provide Series.iteritems for compatibility with older code
from pandas import Series
if not hasattr(Series, "iteritems"):
    Series.iteritems = Series.items
