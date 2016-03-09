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
    def from_uri(cls, uri, box_size=None, translate=None, *args, **kwargs):
        """Load a file.

        :param box_size: three-element array-like used in the scoring command (i.e. half-sizes)
        :param translate: three-element array-like used in the scoring command

        Rotations are not supported.
        If box_size and translate arguments are specified, the following columns are converted: ix => x, iy => y, iz => z
        """
        # TODO: Support rotations to produce x, y, z from ix, iy, iz
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
        if box_size and translate:
            data["ix"] = (data["ix"] - len(data["ix"]) / 2.0 + 0.5) * 2 * box_size[0] / (len(data["ix"])) + translate[0]
            data["iy"] = (data["iy"] - len(data["iy"]) / 2.0 + 0.5) * 2 * box_size[1] / (len(data["iy"])) + translate[1]
            data["iz"] = (data["iz"] - len(data["iz"]) / 2.0 + 0.5) * 2 * box_size[2] / (len(data["iz"])) + translate[2]
            data.rename({"ix" : "x", "iy" : "y", "iz" : "z"}, inplace=True)
        return cls(inner_data=data, uri=uri)
