FROM python:3.12-slim

# Instala locales e configura o locale
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Gera e configura o locale
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

# Define as variáveis de ambiente para o locale
ENV LANG=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt

# Atualiza pip e instala Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copia os arquivos do projeto
WORKDIR /indicadores
COPY . /indicadores

# Instala as dependências (sem tentar instalar o "root package")
RUN poetry install --no-root

# Expõe a porta e executa o Streamlit
EXPOSE 8501
ENTRYPOINT ["poetry","run","streamlit","run","./login.py","--server.port=8501", "--server.address=0.0.0.0" ]