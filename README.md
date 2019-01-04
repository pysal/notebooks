# PySAL Notebooks Project

This project uses [`jupyter-book`](https://github.com/choldgraf/jupyter-book)
to build a book with all the notebooks of the packages in the PySAL
federation. The result is available at:

> [http://darribas.org/notebooks](http://darribas.org/notebooks)

## Dependencies

If you want to access the built book, simply head over to the URL above. If
you want to build the book locally, you will need the following:

* Unix OS: the builder relies on a few shell commands
* `git`
* Python libraries listed in [`build-requirements.txt`](lib/jupyter-book-master/build-requirements.txt)

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



