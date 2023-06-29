import pandas as pd

class DataManipulator:

    @staticmethod
    def getGruppedPercentages(d: pd, denominator: int, groupBy: str="", col_name: str="Percentage"):
        d = d.groupby([groupBy]).size().reset_index(name = col_name)
        d[col_name] = d[col_name] / denominator
        d[col_name] = d[col_name] * 100
        d[col_name] = d[col_name].round().astype(int)
        return d