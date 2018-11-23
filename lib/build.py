import time
import yaml
import os

PKGS_YML = 'packages.yml'
NBS_FOLDER = '../notebooks'
BOOK_FOLDER = '../book'
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
            nbs = [i for i in os.listdir(f'{tmp}/dls/{subpackage}/notebooks') \
                   if i[-6:]=='.ipynb']
            if len(nbs) > 0:
                os.system(f'mkdir -p {tgt_folder}/{package}/{subpackage}/')
                for i in range(len(nbs)):
                    src_nb = nbs[i].replace(' ', '\ ')
                    cmd = (f'mv {tmp}/dls/{subpackage}/notebooks/{src_nb} '\
                           f'{tgt_folder}/{package}/{subpackage}/{src_nb}')
                    os.system(cmd)
            else:
                print((f"\nWARNING: {package}/{subpackage} does NOT"\
                        " contain notebooks\n"))
            break
        break
    os.system(f'rm -rf {tmp}')
    t1 = time.time()
    print(f"\n\t{t1-t0} seconds to collect notebooks")
    return None

def setup_book(bk_folder=BOOK_FOLDER, template_folder=TEMPLATE_FOLDER):
    '''
    Create a new directory, move required files from template, move notebooks
    in
    '''
    os.system(f'rm -rf {BOOK_FOLDER}')
    os.system(f'cp -r {TEMPLATE_FOLDER} {BOOK_FOLDER}')
    os.system(f'rm -r {BOOK_FOLDER}/content')
    os.system(f'cp -r {NBS_FOLDER} {BOOK_FOLDER}/content')
    os.system(f'cp -r {TEMPLATE_FOLDER}/content/intro.md {BOOK_FOLDER}/content')
    os.system(f'python {BOOK_FOLDER}/scripts/generate_book.py')
    return None

if __name__ == '__main__':

    #pull_src_notebooks()
    setup_book()
