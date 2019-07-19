import time
import yaml
import os
import argparse

NBS_FOLDER = './notebooks'
BOOK_FOLDER = './docs'
BASE_TOC = './lib/base_toc.yml'
TEMPLATE_FOLDER = './lib/jupyter-book-master'

def pr(cmd):
    print(cmd)
    os.system(cmd)
    return None

def pull_notebooks(tgt_folder=NBS_FOLDER,
                   tmp='./tmp'):
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
    pr(f'rm -rf {tmp} && mkdir {tmp}')
    pr(f'rm -rf {tgt_folder} && mkdir {tgt_folder}')
    # Grab latest meta package
    cmd = (f'git clone https://github.com/pysal/pysal.git '\
           f'{tmp}/dls/')
    pr(cmd)
    # Copy notebooks to tgt_folder
    cmd = f'mv {tmp}/dls/notebooks/* {tgt_folder}/'
    pr(cmd)
    t1 = time.time()
    print(f"\nNew notebooks collected in {round(t1-t0)} seconds")
    return None

def setup_book(bk_folder=BOOK_FOLDER, nbs_folder=NBS_FOLDER):
    '''
    Create a new directory, move required files from template, move notebooks
    in
    '''
    # Clean slate
    pr(f'rm -rf {bk_folder}')
    # Create book
    pr((f'jupyter-book create {bk_folder} '\
        f'--content-folder {nbs_folder} '\
        f'--verbose yes'))
    # Build TOC + write into book
    toc = build_toc(BASE_TOC)
    fo = open(f'{bk_folder}/_data/toc.yml', 'w')
    fo.write(toc)
    fo.close()
    pr(f'jupyter-book build {bk_folder}')
    return toc

def build_toc(base_toc, nbs_folder=NBS_FOLDER):
    '''
    Auto-generate TOC for notebooks folder
    '''
    fo = open(base_toc, 'r')
    toc = fo.read()
    fo.close()
    toc += '\n# Built Automatically #\n'

    folders = os.listdir(nbs_folder)
    for folder in folders:
        # Add Separator
        sec_title = folder[0].upper() + folder[1:]
        toc += build_entry(divider=True, header=sec_title)
        # Add line for every notebook
        for pkg in os.listdir(nbs_folder+'/'+folder):
            nbs = [i for i in os.listdir(f'{nbs_folder}/{folder}/{pkg}') \
                   if i[-6:]=='.ipynb']
            sections = ''
            for nb in nbs:
                sections += build_entry(nb.replace('.ipynb', ''), 
                                        f'/{folder}/{pkg}/{nb.replace(".ipynb", "")}')
            sections = sections.replace('\n\n', '\n').replace('\n', '\n  ')
            # Build PKG entry
            toc += build_entry(pkg, f'/{folder}/{pkg}/intro',
                    sections=sections, not_numbered=True)
    return toc

def build_entry(title=None, url=None, clas=None, sections=None, not_numbered=False,
        divider=False, header=None):
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Pull notebooks/build book")
    parser.add_argument('--pull', 
                        help='Download notebooks from federated packages',
                        action="store_true")
    parser.add_argument('--build', 
                        help='Build book',
                        action="store_true")
    args = parser.parse_args()

    if args.pull:
        pull_src_notebooks()
    if args.build:
        toc = setup_book()

