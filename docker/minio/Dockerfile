FROM golang:1.24.8-bookworm AS builder

WORKDIR /src

RUN git clone --depth 1 \
    --branch RELEASE.2025-10-15T17-29-55Z \
    https://github.com/minio/minio.git .

RUN test "$(git rev-parse HEAD)" = \
    "9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a"

RUN CGO_ENABLED=0 go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /out/minio .

FROM debian:bookworm-slim

COPY --from=builder /out/minio /usr/local/bin/minio

RUN mkdir /data && chown 10001:10001 /data

USER 10001:10001

EXPOSE 9000 9001

ENTRYPOINT ["/usr/local/bin/minio"]