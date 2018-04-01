from plumbum import cli

class Json2Pandas(cli.Application):

    json_dir = cli.SwitchAttr(
        ['--json_dir'],
        argtype=str,
        mandatory=True,
        help='Path to directory of json files',
    )
    
    output = cli.SwitchAttr(
        ['--output'],
        argtype=str,
        mandatory=True,
        help='Path to desired dataframe (pkl) output',
    )

    def main(self):
        import numpy as np
        import pandas as pd
        from os import path
        from pandas.io.json import json_normalize
        from glob import glob
        import json

        data = []
        for file_name in glob(path.join(self.json_dir, '*.json')):
            with open(file_name) as f:
                data.append(json.load(f))

        df = pd.DataFrame(data=json_normalize(data))
        df.to_pickle(self.output)


if __name__ == '__main__':
    Json2Pandas.run()
