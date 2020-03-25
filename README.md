# PySAL Notebooks Project

This project uses [`jupyter-book`](https://github.com/choldgraf/jupyter-book)
to build a book with all the notebooks of the packages in the PySAL
federation. The result is available at:

> [http://pysal.org/notebooks](http://pysal.org/notebooks)

## Dependencies

If you want to access the built book, simply head over to the URL above. If
you want to build the book locally, you will need the following:

* A recent version of `jupyter-book`
* Unix OS: the builder relies on a few shell commands (`rm`, `mkdir`, `cp`, `mv`, `cd`)
* `pandoc` (for `.rst` to `.md` conversion)
* `git`
* Python libraries listed in [`build-requirements.txt`](lib/jupyter-book-master/build-requirements.txt)

A recommended route is to run this repository inside a [`gds_env`](https://github.com/darribas/gds_env) 
(use the `gds_dev` flavour) container, which is the platform used to build it. If you have it installed,
you can launch it from the `notebooks` folder by running:

```
> docker run --rm -ti -p 8888:8888 -p 4000:4000 -v ${PWD}:/home/jovyan/work darribas/gds_dev:4.0
```

## Build process

The current build process involves two main steps:

1. Pull repositories to extract the files used to build the book. This can be
   done by running the following command from the root folder:

   `> python lib/build.py --pull`

   This will generate a `notebooks` folder that contains all the files
   required to build the book.
1. Build the book from the downloaded notebooks. This can be  done by running
   the following command from the root folder:

   `> python lib/build.py --build`

   This will create/update the `docs` folder in the root folder so it contains
   everything needed for the hosting server to serve the book. Commit the
   changes and the updated book will be available online shortly.
   
The built website is available on the `./docs` folder and is ready to be pushed to the repository 
for serving on Github Pages. If you want to serve it locally, you will need to:

1. Navigate into the `./docs` directory:

    `> cd docs`
    
1. Serve the site:

    `> jekyll serve`
    
    If you are serving it inside a container, fix the host so it can be accessed from the host machine:

    `> jekyll serve --host="0.0.0.0"`
    
    Then point your browser to `localhost:4000/notebooks/`
        
Additionally, the command line tool `lib/build.py` incorporates experimental support for testing
the notebooks. Again, two options are available:

1. Test all the `.ipynb` files are well-formated and can be converted:

    `> python lib/build.py --test_no_run`

1. Execute all the `.ipynb` files:

    `> python lib/build.py --test_run`



