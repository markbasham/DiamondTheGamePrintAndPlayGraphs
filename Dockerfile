FROM continuumio/miniconda3

COPY . .

RUN conda install notebook pandas matplotlib

EXPOSE 8890

CMD ["jupyter", "notebook", "--no-browser", "--allow-root", "--ip=0.0.0.0", "--port=8890", "--NotebookApp.token=''", "--NotebookApp.password=''", "/local"]