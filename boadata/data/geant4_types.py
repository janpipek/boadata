"""Classes useful for analysis of data obtained from Geant4.

Currently, this includes just CSV-like files from command-based scoring."""
from boadata.core import DataObject
from .xarray_types import XarrayDatasetBase
import codecs
import xarray as xr


@DataObject.register_type()
class Geant4Scoring(XarrayDatasetBase):
    """Geant4 command-based scoring output file."""
    type_name = "geant4_scoring"

    @classmethod
    def from_uri(cls, uri, *args, **kwargs):
        import pandas as pd
        mesh_name = ""
        scorers = []
        with codecs.open(uri) as f:
            for i, line in enumerate(f):
                if line.startswith("# mesh name: "):
                    mesh_name = line.split(":", 2)[-1].strip()
                if line.startswith("# primitive scorer name: "):
                    scorer_name = line.split(":", 2)[-1].strip()
                    scorers.append([scorer_name, i + 2, None])
                    if len(scorers) > 1:
                        scorers[-2][2] = i
        scorers[-1][2] = i + 1
        df = pd.DataFrame()
        for scorer in scorers:
            scorer_df = pd.read_csv(uri, skiprows=scorer[1], names=["ix", "iy", "iz", scorer[0]], index_col=[0, 1, 2],
                                    nrows=scorer[2] - scorer[1])
            df[scorer[0]] = scorer_df[scorer[0]]
        data = xr.Dataset.from_dataframe(df)
        return cls(inner_data=data, uri=uri)
