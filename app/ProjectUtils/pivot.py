import pandas as pd
import numpy as np
import random
from app import app
import os
from flask_login import current_user


class Pivot():

    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.filename = str(current_user.id)+str(random.randint(1, 1000))+"PivotResult.xlsx"

        

    def get_pivot(self):
        result = self.df.pivot_table(index=["Category", "Segment"], values=["Sales", "Quantity"], aggfunc={"Sales":[np.sum, np.average],"Quantity":[np.sum]})
        try:
            __path = os.path.join(app.config["UPLOAD_FOLDER"])+"/"+self.filename
            result.to_excel(__path)
            return self.filename
        except:
            return False

