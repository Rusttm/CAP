FROM apache/airflow:latest-python3.10
COPY requirements.txt /opt/airflow/config/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/airflow/config/requirements.txt


# create venv for sqlalchemy
# from https://github.com/astronomer/astro-provider-venv
USER root
RUN mkdir -p /home/cap_enviroments/.venv/sqlalchemy
COPY venv_requirements.txt /home/cap_enviroments/.venv/sqlalchemy/requirements.txt
RUN /usr/local/bin/python -m venv --system-site-packages /home/cap_enviroments/.venv/sqlalchemy
ENV ALCHEMY_PYENV /home/cap_enviroments/.venv/sqlalchemy/bin/python
RUN --mount=type=cache,target=/home/cap_enviroments/.cache/pip /home/cap_enviroments/.venv/sqlalchemy/bin/pip --cache-dir=/home/cap_enviroments/.cache/pip install -r /home/cap_enviroments/.venv/sqlalchemy/requirements.txt


