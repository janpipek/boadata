from boadata.core import DataObject
from  .plotting_types import XYPlotDataSeriesBase
from .numpy_types import NumpyArrayBase


@DataObject.register_type()
class MatlabFigXYData(XYPlotDataSeriesBase):
    type_name = "matlab_fig_xy"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and uri.endswith(".fig")

    @classmethod
    def _from_matlab73(cls, uri, **kwargs):
        import pydons
        fb = pydons.FileBrowser(uri, any_keys=True)
        x = None
        y = None
        xlabel = "x"
        ylabel = "y"

        for key, value in fb["#refs#"].items():
            if not isinstance(value, pydons.MatStruct):
                continue
            if "properties" in value:
                if "XData" in value.properties and "YData" in value.properties and "ZData" not in value.properties:
                    x = value.properties.XData
                    y = value.properties.YData

        if x is not None and y is not None:
            return cls(x=x, y=y, xname=xlabel, yname=ylabel, uri=uri)
        else:
            raise RuntimeError("No suitable figures found in {0}".format(uri))

    @classmethod
    def _from_oldmatlab(cls, uri, **kwargs):
        from scipy.io import loadmat
        from numpy import size
        data = loadmat(uri, squeeze_me=True, struct_as_record=False)

        ax1 = data['hgS_070000'].children
        if size(ax1) > 1:
            ax1 = ax1[0]

        x = None
        y = None
        xlabel = "x"
        ylabel = "y"

        counter = 0
        for line in ax1.children:
            if line.type == 'graph2d.lineseries':
                x = line.properties.XData
                y = line.properties.YData
            elif line.type == 'text':
                if counter == 0:
                    # name of the plot?
                    pass
                if counter == 1:
                    xlabel = str(line.properties.String)
                elif counter == 2:
                    ylabel = str(line.properties.String)
                counter += 1

        if x is not None and y is not None:
            return cls(x=x, y=y, xname=xlabel, yname=ylabel, uri=uri)
        else:
            raise RuntimeError("No suitable figures found in {0}".format(uri))

    @classmethod
    def from_uri(cls, uri, **kwargs):
        try:
            return cls._from_oldmatlab(uri, **kwargs)
        except:
            try:
                return cls._from_matlab73(uri, **kwargs)
            except:
                raise RuntimeError("Cannot interpret MATLAB figure {0}".format(uri))


@DataObject.register_type()
class OldMatlabData(NumpyArrayBase):
    type_name = "matlab_data"

    @classmethod
    def accepts_uri(cls, uri):
        if not uri:
            return False
        frags = uri.split("::")
        if len(frags) != 2:
            return False
        file, _ = frags
        return file.endswith(".mat")

    @classmethod
    def from_uri(cls, uri, **kwargs):
        from scipy.io import loadmat
        file, key = uri.split("::")
        data = loadmat(file)
        inner_path = key.split("/")
        for item in inner_path:
            data = data[item]
        return cls(inner_data=data, uri=uri)
