# Introduction
## Installation
Requires working ingress controller + CertManager with Letsencrypt support.

```console
./create_namespace.sh
./install.sh
```
# How to copy data to S3?
## Set Minio alias
```console
mc alias set minio https://s3.minio.domain.com:9000 admin secret_password_from_bitwarden --insecure
```

## Sync files from Dropbox
```console
mc mb myminio/mybucket --insecure
mc mirror /data myminio/mybucket --insecure 
```

## Remove entire bucket
```console
mc rb --force --dangerous --insecure minio/mybucket
```
