FROM apache/airflow:latest-python3.10
COPY requirements.txt /opt/airflow/config/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/airflow/config/requirements.txt

# create user
ARG USER=airflow
ARG UID=1000
ARG GID=100
ARG TINI=v0.18.0
ARG ENV_NAME=alchemy

ENV ENV_DIR /opt/venvs/${ENV_NAME}


# Create user and setup permissions on /etc/sudoers
#RUN useradd -m -s /bin/bash -N -u $UID $USER && \
#    echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
#    chmod 0440 /etc/sudoers && \
#    chmod g+w /etc/passwd
#RUN echo 'root:Docker!' | chpasswd

# create venv for sqlalchemy
# from https://github.com/astronomer/astro-provider-venv
#USER ${USER}

USER root
WORKDIR $ENV_DIR
COPY venv_requirements.txt $ENV_DIR/requirements.txt
RUN python -m venv --system-site-packages $ENV_DIR
#ENV PATH="$ENV_DIR/bin:$PATH"
ENV ALCHEMY_PYENV $ENV_DIR/bin/python
RUN --mount=type=cache,target=$ENV_DIR/.cache/pip $ENV_DIR/bin/pip --cache-dir=$ENV_DIR/.cache/pip install -r $ENV_DIR/requirements.txt
#RUN source $ENV_DIR/bin/activate && pip install -r $ENV_DIR/requirements.txt
#RUN deactivate
# runs only with buildkit https://docs.docker.com/build/buildkit/
# PYENV 3.10 cap_venv venv_requirements.txt