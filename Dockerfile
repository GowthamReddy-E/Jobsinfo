FROM nginx
COPY index.html /usr/share/nginx/html/index.html
LABEL maintainer="gowthamreddy.6991@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python"]
CMD ["src/app.py"]