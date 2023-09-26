FROM continuumio/miniconda3

COPY . .

# Create a geopandas enviroment for the location plots
RUN conda create -n geopandas geopandas

#create a pandas and jupyter enviroment for most of the plots as the default
RUN conda install pandas notebook pandas matplotlib
RUN conda install -c conda-forge wordcloud

RUN conda init bash

EXPOSE 8080

CMD ["jupyter", "notebook", "--no-browser", "--allow-root", "--ip=0.0.0.0", "--port=8080", "--NotebookApp.token=''", "--NotebookApp.password=''", "/local"]