# To compile this with docker use:
# docker build --tag turbo_seti .
# Then to run it:
# docker run --rm -it turbo_seti
# To be able to access local disk on Mac OSX, you need to use Docker for Mac GUI
# and click on 'File sharing', then add your directory, e.g. /data/bl_pks
# Then to run it:
# docker run --rm -it -v /data/bl_pks:/mnt/data turbo_seti
# And if you want to access a port, you need to do a similar thing:
# docker run --rm -it -p 9876:9876 sigpyproc

FROM python:latest
ARG DEBIAN_FRONTEND=noninteractive

ENV TERM xterm

#####
# Pip installation of python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools wheel
RUN python3 -m pip install numpy
RUN python3 -m pip install pandas cython astropy matplotlib 
RUN python3 -m pip install astroquery
RUN python3 -m pip install --only-binary=scipy scipy
RUN python3 -m pip install pytest
RUN python3 -m pip install dask 
RUN pip3 install git+https://github.com/pydata/xarray
RUN python3 -m pip install "dask[bag]" --upgrade
RUN python3 -m pip install jupyter
#RUN python3 -m pip install git+https://github.com/UCBerkeleySETI/blimpy
RUN pip3 install git+https://github.com/UCBerkeleySETI/blimpy
RUN pip3 install git+https://github.com/UCBerkeleySETI/turbo_seti
#RUN python3 -m pip install turbo-seti
#RUN python3 -m pip install colorama
#RUN python3 -m pip install bokeh
RUN pip3 install git+https://github.com/bbrzycki/setigen
#RUN python3 -m pip install setigen


