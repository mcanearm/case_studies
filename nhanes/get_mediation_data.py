"""Download the 2017–2018 files needed by sodium_mediation.ipynb."""
from pathlib import Path
from io import BytesIO
import pandas as pd
import requests

DATA = Path(__file__).resolve().parent / '2017'
FILES = ['DEMO_J', 'BPX_J', 'BMX_J', 'DR1TOT_J', 'BPQ_J']


def download():
    DATA.mkdir(exist_ok=True)
    for name in FILES:
        target = DATA / f'{name}.xpt'
        if target.exists():
            frame = pd.read_sas(target, format='xport')
        else:
            url = f'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/{name}.xpt'
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            # Parse before saving: CDC error pages sometimes return HTTP 200.
            frame = pd.read_sas(BytesIO(response.content), format='xport')
            target.write_bytes(response.content)
        if not frame.SEQN.is_unique:
            raise ValueError(f'Duplicate participant identifiers in {name}')
        frame.to_csv(DATA / f'{name}.csv.gz', index=False)
        print(f'{name}: {len(frame):,} participants')


if __name__ == '__main__':
    download()
