FROM python:3.8
COPY requirements.txt /ECommerce/
WORKDIR /ECommerce
RUN pip install -r requirements.txt
ADD . /ECommerce
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]