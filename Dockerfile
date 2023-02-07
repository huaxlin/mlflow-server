FROM python:3.10

# Setup Pypi
ARG PyPI_CN_HOST=pypi.doubanio.com
ARG PyPI_CN_REPO=https://${PyPI_CN_HOST}/simple
#ARG PyPI_PRI_HOST=pypi.private.com
#ARG PyPI_PRI_REPO=http://${PyPI_PRI_HOST}/root/public/+simple

RUN echo "[global]" > /etc/pip.conf \
 && echo "index-url = ${PyPI_CN_REPO}" >> /etc/pip.conf \
# && echo "extra-index-url = ${PyPI_PRI_REPO}" >> /etc/pip.conf \
 && echo "[install]" >> /etc/pip.conf \
 && echo "trusted-host = ${PyPI_CN_HOST}" >> /etc/pip.conf \
# && echo "               ${PyPI_PRI_HOST}" >> /etc/pip.conf \
 && python -m pip install -U pip \
 && python -m pip install wheel
ENV TZ=Asia/Shanghai


WORKDIR /code

# Install python packages
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
