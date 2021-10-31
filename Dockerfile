# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pipenv install
RUN python -m pipenv shell

WORKDIR /app
COPY . /app

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

RUN apt update -y && \
    apt install -y git curl zsh sudo && \
    curl -L git.io/antigen > /home/appuser/antigen.zsh && \
    curl -L https://gitlab.com/-/snippets/2163394/raw/main/.zshrc?inline=false > /home/appuser/.zshrc

USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
