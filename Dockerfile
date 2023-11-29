FROM python:3.9
LABEL authors="frzf7"
WORKDIR /app

# Add PostgreSQL repository and install PostgreSQL 16

# Install Python dependencies using pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copy the content of the local src directory to the working directory
COPY . .
EXPOSE 8000
