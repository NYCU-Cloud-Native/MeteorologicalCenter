FROM rust:1.70 AS Build

WORKDIR /app

COPY . .

RUN apt update && apt install -y protobuf-compiler

RUN cargo build -r

FROM debian:bullseye AS Production

WORKDIR /app

COPY --from=Build /app/target/release/controller /app

CMD ["./controller"]