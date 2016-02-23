from boadata.core import DataObject
from  .plotting_types import XYPlotDataSeriesBase


@DataObject.register_type()
class MatlabFigXYData(XYPlotDataSeriesBase):
    type_name = "matlab_fig_xy"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and uri.endswith(".fig")

    @classmethod
    def from_uri(cls, uri, **kwargs):
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
