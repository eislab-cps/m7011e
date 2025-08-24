# How setup CertManager with Letsencrypt?
## RKE2 with Nginx
```console
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.10.0/cert-manager.yaml
kubectl create -f letsencrypt.yaml
```

## K3s with Traefik 
```console
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.10.0/cert-manager.yaml
kubectl create -f letsencrypt_k3s.yaml
```

# Verify installation
```console
 kubectl get pods --namespace cert-manager
```
 
Should print:
```console
NAME                                     READY   STATUS    RESTARTS   AGE
cert-manager-646dddd544-rrmx4            1/1     Running   0          19h
cert-manager-cainjector-8676c4b7-dxsjw   1/1     Running   0          19h
```
 
# Get info about a certificate
```console
kubectl get certificate
kubectl describe CertificateRequest -n test
```
