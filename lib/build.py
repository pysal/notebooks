import time
import yaml
import os

PKGS_YML = 'packages.yml'
NBS_FOLDER = '../notebooks'
BOOK_FOLDER = '../docs'
TEMPLATE_FOLDER = './jupyter-book-master'

def pull_src_notebooks(pkgs=PKGS_YML, tgt_folder=NBS_FOLDER,
                       tmp='./tmp'):
    '''
    Download Master branch from each package, extract notebooks and move to
    target folder
    ...

    Arguments
    ---------
    pkgs        : str
                  Path to YAML file
    tgt_folder  : str
                  Path to target folder to put renamed notebooks

    Returns
    -------
    None
    '''
    with open(pkgs) as package_file:
        packages = yaml.load(package_file)

    os.system(f'rm -rf {tmp} && mkdir {tmp}')
    os.system(f'rm -rf {tgt_folder} && mkdir {tgt_folder}')

    t0 = time.time()
    for package in packages:
        subpackages = packages[package].split()
        for subpackage in subpackages:
            cmd = (f'git clone https://github.com/pysal/{subpackage}.git '\
                   f'{tmp}/dls/{subpackage}')
            os.system(cmd)
            nbf_exists = True
            try:
                os.listdir(f'{tmp}/dls/{subpackage}/notebooks')
            except:
                nbf_exists = False
                print((f"\nWARNING: {package}/{subpackage} does NOT"\
                        " contain a notebook folder\n"))
            if nbf_exists:
                # Collect individual notebooks (if needed, they can be
                # filtered here easily)
                nbs = [i for i in os.listdir(f'{tmp}/dls/{subpackage}/notebooks') \
                       if i[-6:]=='.ipynb']
                if len(nbs) > 0:
                    os.system(f'mkdir -p {tgt_folder}/{package}/{subpackage}/')
                    # Process README as intro in the book
                    os.system((f'cp {tmp}/dls/{subpackage}/README.md '\
                               f'{tgt_folder}/{package}/{subpackage}/intro.md'))
                    ## If .rst
                    os.system((f'pandoc -s {tmp}/dls/{subpackage}/README.rst '\
                               f'-o {tgt_folder}/{package}/{subpackage}/intro.md'))
                    # Copy individual notebooks
                    for i in range(len(nbs)):
                        src_nb = nbs[i].replace(' ', '\ ')
                        cmd = (f'mv {tmp}/dls/{subpackage}/notebooks/{src_nb} '\
                               f'{tgt_folder}/{package}/{subpackage}/'\
                               f'{src_nb.replace(" ", "_")}')
                        os.system(cmd)
                else:
                    print((f"\nWARNING: {package}/{subpackage} does NOT"\
                            " contain notebooks\n"))
    os.system(f'rm -rf {tmp}')
    t1 = time.time()
    print(f"\n\t{t1-t0} seconds to collect notebooks")
    return None

def setup_book(bk_folder=BOOK_FOLDER, nbs_folder=NBS_FOLDER, template_folder=TEMPLATE_FOLDER):
    '''
    Create a new directory, move required files from template, move notebooks
    in
    '''
    os.system(f'rm -rf {bk_folder}')
    os.system(f'cp -r {template_folder} {bk_folder}')
    os.system(f'cp -r {nbs_folder}/* {bk_folder}/content/')
    toc = build_toc(f'{TEMPLATE_FOLDER}/_data/toc.yml')
    fo = open(f'{bk_folder}/_data/toc.yml', 'w')
    fo.write(toc)
    fo.close()
    os.system(f'cd {bk_folder} && make book')
    return toc

def build_toc(base_toc, nbs_folder=NBS_FOLDER):
    '''
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

    #pull_src_notebooks()
    toc = setup_book()
    #print(toc)
