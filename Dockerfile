FROM python:3.8

ENV FLASK_APP="editoggia"
EXPOSE 5000

RUN useradd --create-home editoggia
WORKDIR /home/editoggia
USER editoggia
ENV PATH="/home/editoggia/.local/bin:${PATH}"

# Install dependencies
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY --chown=editoggia . .

CMD ["flask", "run", "--host", "0.0.0.0"]
