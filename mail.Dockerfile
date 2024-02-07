FROM python:3.10


# Install the desired version of OpenSSL
RUN apt-get update
RUN apt-get -y install gcc g++ gfortran git patch wget pkg-config liblapack-dev libmetis-dev liblapack-dev
RUN apt-get -y install automake autoconf libtool
# Install OpenSSL 1.1.1s

# Download and extract OpenSSL source code
RUN curl -LO https://www.openssl.org/source/openssl-1.1.1s.tar.gz && \
    tar -xzf openssl-1.1.1s.tar.gz && \
    cd openssl-1.1.1s

# Configure, build, and install OpenSSL
RUN cd openssl-1.1.1s && \
    ./config && \
    make && \
    make install

# Set the environment variables to use the newly installed OpenSSL
ENV LD_LIBRARY_PATH="/usr/local/ssl/lib"
ENV LDFLAGS="-L/usr/local/ssl/lib"
ENV CPPFLAGS="-I/usr/local/ssl/include"


COPY .env ./
COPY main.py read_mail.py mail-requirements.txt  ./
RUN pip install --upgrade pip
RUN pip install -r mail-requirements.txt



CMD ["python","main.py"]