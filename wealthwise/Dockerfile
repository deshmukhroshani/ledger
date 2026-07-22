FROM python:3.10

EXPOSE 8080
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt
RUN pip install pycountry
RUN pip install psycopg2

ENTRYPOINT ["streamlit", "run", "landing_page.py", "--server.port=8080", "--server.address=0.0.0.0"]
