import os
import time
import zipfile
import requests
import argparse
import subprocess
from tqdm import tqdm
from pathlib import Path

NBS_FOLDER = './notebooks'
BOOK_FOLDER = './docs'
TEMPLATE_FOLDER = './lib/template_data'


def pr(cmd, throw_error=False):
    print(cmd)
    #os.system(cmd)
    op = subprocess.run(cmd, capture_output=True, shell=True)
    if op.stderr:
        print('\n### Log Msg. ###')
        print(op.stderr.decode())
        print('\n')
        if throw_error:
            raise
    return None


def wr(content, path):
    fo = open(path, 'w')
    fo.write(content)
    fo.close()
    return None

def download_file_pb(url, f_path):
    '''
    Download a file using tqdm progressbar
    ...
    
    NOTE: taken mostly from:
    
    > https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
    '''
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('Content-Length', 0))
    block_size = 1024 #1 Kibibyte
    t=tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(f_path, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        raise ValueError("ERROR, something went wrong")
    return None

def pull_notebooks(tgt_folder=NBS_FOLDER, tmp='./tmp'):
    '''
    Download Master branch from meta package, extract notebooks and move to
    target folder
    ...

    Arguments
    ---------
    tgt_folder  : str
                  Path to target folder to put renamed notebooks
    tmp         : str
                  [Optional. Default='./tmp'] Location of temporary folder

    Returns
    -------
    None
    '''
    t0 = time.time()
    # Clean start
    pr(f'rm -rf {tmp}')
    pr(f'mkdir {tmp}')
    pr(f'rm -rf {tgt_folder}')
    pr(f'mkdir {tgt_folder}')
    # Grab latest meta package
    url = "https://github.com/pysal/pysal/archive/master.zip"
    z_file = f"{tmp}/master.zip"
    print(f"Downloading {url}")
    _ = download_file_pb(url, z_file)
    zip_ref = zipfile.ZipFile(z_file, 'r')
    zip_ref.extractall(f"{tmp}/dls/")
    zip_ref.close()
    # Pre-process file names
    all_ipynbs = list(Path(f"{tmp}/dls/pysal-master/notebooks").rglob("*.ipynb"))
    for nb in all_ipynbs:
        nb = str(nb)
        if nb != nb.replace(' ', '_'):
            print(f"Renaming {nb}")
            wr(open(nb).read(), nb.replace(' ', '_'))
            nb_f = nb.replace(' ', '\ ')
            os.system(f"rm {nb_f}")
    # Copy notebooks to tgt_folder
    cmd = f'mv {tmp}/dls/pysal-master/notebooks/* {tgt_folder}/'
    pr(cmd)
    # Clean up
    pr(f"rm -r {tmp}")
    t1 = time.time()
    print(f"\nNew notebooks collected in {round(t1-t0)} seconds")
    return None


def test_notebooks(nbs_folder=NBS_FOLDER, execute=True):
    '''
    Execute notebooks in `nbs_folder`
    ...

    Arguments
    ---------
    nbs_folder  : str
    execute     : Boolean

    Returns
    -------
    None
    '''
    all_ipynbs = list(Path(nbs_folder).rglob("*.ipynb"))
    for nb in all_ipynbs:
        nb = str(nb)
        cmd = f"jupyter nbconvert --to markdown --stdout {nb}"
        if execute:
            cmd += ' --execute'
        pr(cmd)
    return None

def setup_book(bk_folder=BOOK_FOLDER, nbs_folder=NBS_FOLDER):
    '''
    Create a new directory, move required files from template, move notebooks
    in and build book
    ...

    Arguments
    ---------
    bk_folder   : str
    nbs_folder  : str

    Return
    ------
    None
    '''
    # Clean slate
    pr(f'rm -rf {bk_folder}')
    # Create book
    pr((f'jupyter-book create '\
        f'--content-folder {nbs_folder} '\
        f'--verbose '\
        f'{bk_folder}'))
    # Build TOC + write into book
    toc = build_toc(f"{TEMPLATE_FOLDER}/base_toc.yml")
    wr(toc, f'{bk_folder}/_data/toc.yml')
    # Intro
    pr(f'cp {TEMPLATE_FOLDER}/intro.md {bk_folder}/content/intro.md')
    # Package intros
    intro_paths = parse_toc_intro(toc, f"{bk_folder}/content")
    for pkg in intro_paths:
        _ = write_pkg_intro(pkg, intro_paths[pkg])
    # Config, logo, favicon
    pr(f'cp {TEMPLATE_FOLDER}/_config.yml {bk_folder}/_config.yml')
    pr(f'cp {TEMPLATE_FOLDER}/logo.png {bk_folder}/assets/images/logo.png')
    pr(f'cp {TEMPLATE_FOLDER}/pysal_favicon.ico {bk_folder}/assets/images/pysal_favicon.ico'
       )
    # Build book
    pr(f'jupyter-book build {bk_folder}')
    return None


def build_toc(base_toc, nbs_folder=NBS_FOLDER):
    '''
    Auto-generate TOC for notebooks folder
    '''
    fo = open(base_toc, 'r')
    toc = fo.read()
    fo.close()
    toc += '\n# Built Automatically #\n'

    folders = [i for i in os.listdir(nbs_folder) if \
                os.path.isdir(f"{nbs_folder}/{i}")]
    for folder in folders:
        # Add Separator
        sec_title = folder[0].upper() + folder[1:]
        toc += build_entry(divider=True, header=sec_title)
        # Add line for every notebook
        pkgs = [i for i in os.listdir(nbs_folder+'/'+folder) if \
                os.path.isdir(f"{nbs_folder}/{folder}/{i}")]
        for pkg in pkgs:
            nbs = [i for i in os.listdir(f'{nbs_folder}/{folder}/{pkg}') \
                   if i[-6:]=='.ipynb']
            sections = ''
            for nb in nbs:
                sections += build_entry(
                    nb.replace('.ipynb', ''),
                    f'/{folder}/{pkg}/{nb.replace(".ipynb", "")}')
            sections = sections.replace('\n\n', '\n').replace('\n', '\n  ')
            # Build PKG entry
            toc += build_entry(pkg,
                               f'/{folder}/{pkg}/intro',
                               sections=sections,
                               not_numbered=True)
    return toc


def build_entry(title=None,
                url=None,
                clas=None,
                sections=None,
                not_numbered=False,
                divider=False,
                header=None):
    '''
    Build entry in toc file
    '''
    entry = '\n'
    if title:
        entry += f'- title: {title}\n'
        if url:
            entry += f'  url: {url}\n'
        if clas:
            entry += f'  class: {clas}\n'
        if not_numbered:
            entry += f'  not_numbered: true\n'
        if sections:
            entry += f'  sections:{sections}'
    if divider:
        entry += '- divider: true\n'
    if header:
        entry += f'- header: {header}\n'
    return entry


def parse_toc_intro(toc, base_path):
    lines = toc.split('\n')
    intros = {}
    for line in lines:
        if ('/intro' in line) and ('url: /intro' not in line):
            dom, pkg = line.replace('  url: /', '')\
                           .replace('/intro', '')\
                           .split('/')
            intros[pkg] = f"{base_path}/{dom}/{pkg}/intro.md"
    return intros


def write_pkg_intro(pkg, path):
    url = f"https://raw.githubusercontent.com/pysal/{pkg}/master/README.md"
    print(f"\tGetting {url} into\n\t\t{path}")
    wr(requests.get(url).content.decode(), path)
    return path


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Pull notebooks/build book")
    parser.add_argument('--pull',
                        help='Download notebooks from federated packages',
                        action="store_true")
    parser.add_argument('--build', 
                        help='Build book',
                        action="store_true")
    parser.add_argument('--test_no_run',
                        help='Test notebook conversion without executing notebooks',
                        action="store_true")
    parser.add_argument('--test_run',
                        help='Test notebook conversion executing notebooks',
                        action="store_true")
    args = parser.parse_args()

    if args.pull:
        pull_notebooks()
    if args.build:
        toc = setup_book()
    if args.test_no_run:
        test_notebooks(execute=False)
    if args.test_run:
        test_notebooks(execute=True)

