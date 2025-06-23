# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8001

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "my_ecommerce.wsgi"] 