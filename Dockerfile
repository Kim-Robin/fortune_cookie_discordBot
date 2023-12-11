# Stage 1: Build the application
FROM python:3.11.6 as builder

WORKDIR /app

# Copy only the files needed for installing dependencies
COPY pyproject.toml poetry.lock ./

RUN apt-get update 
RUN apt-get install -y curl 
RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev
RUN apt-get install build-essential
RUN apt-get install cargo
RUN rm -rf /var/lib/apt/lists/*
# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"


RUN pip install -U pip setuptools
RUN pip install --upgrade cffi
RUN pip install cryptography

# Install dependencies
RUN pip install --no-cache-dir poetry
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . .

# Build the application (adjust the command based on your build process)
RUN poetry build

# Stage 2: Create a smaller image
FROM python:3.11.6-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app/dist /app/dist

# Copy fortune.json and set environment for it
COPY ./src/scraper/fortune.json /app/dist
ENV FORTUNE_LOCATION=/app/dist/fortune.json


# Install only the necessary runtime dependencies
RUN pip install --no-cache-dir /app/dist/*.whl

# Define the command to run your application
CMD ["bot"]


# Install any needed packages specified in requirements.txt
# RUN pip install poetry
# RUN pip install --no-cache-dir -e .
# RUN poetry install

# Define the command to run your application
# CMD ["poetry", "run", "python_docker"]
