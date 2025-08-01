# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Render will bind to this)
EXPOSE 10000

# Start command (used by Render)
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]
