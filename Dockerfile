FROM prefecthq/prefect:master
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

# see https://developer.feedforce.jp/entry/2021/03/15/102530
# export PREFECT_API_KEY="[KEY] && DOCKER_BUILDKIT=1 docker build --secret id=my_env1,env=PREFECT_API_KEY --no-cache --progress=plain .
RUN --mount=type=secret,id=my_env1 prefect auth login --key `cat /run/secrets/my_env1`

ENTRYPOINT [ "prefect", "agent", "local" ]
CMD ["start"]

EXPOSE 8080
RUN uvicorn main:app --host 0.0.0.0 --port 8080