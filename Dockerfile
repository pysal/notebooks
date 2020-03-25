FROM darribas/gds_py:4.0

# Local docs
RUN rm -R work/
COPY ./docs/content/intro.md ${HOME}/README.md
RUN mkdir ${HOME}/content
COPY ./docs/content/ ${HOME}/content/
RUN rm ${HOME}/content/intro.md
# Fix permissions
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
