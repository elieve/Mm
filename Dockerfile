FROM kynan1503/ubot:final

COPY . /app/
WORKDIR /app/


CMD ["bash", "start"]