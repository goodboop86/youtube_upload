FROM prefecthq/prefect:master
USER root

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY . .
RUN pip install -r requirements.txt

# see https://developer.feedforce.jp/entry/2021/03/15/102530
# export PREFECT_API_KEY="[KEY]
# DOCKER_BUILDKIT=1 docker build --secret id=my_env1,env=PREFECT_API_KEY -t goodboop86/prefect:latest --no-cache --progress=plain .
RUN --mount=type=secret,id=my_env1 prefect auth login --key $(cat /run/secrets/my_env1)

# https://ahmet.im/blog/cloud-run-multiple-processes-easy-way/
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static /tini
RUN chmod +x /tini


# prefect ENV
ENV PREFECT__LOGGING__LEVEL="INFO"
ENV PREFECT__LOGGING__FORMAT="[%(asctime)s] %(levelname)s - %(name)s | %(message)s"

EXPOSE 8080
# RUN sed -i -e "s/PORT/$PORT/g" start.sh
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app
RUN ["chmod", "+x", "./start.sh"]
ENTRYPOINT ["/tini", "--", "./start.sh"]
