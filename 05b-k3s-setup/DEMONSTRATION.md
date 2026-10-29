# Mandatory Kubernetes Environment Demonstration — 13 November 2026

Demonstrate your group's environment to **Casper Lundberg on Friday 13 November**. Prepare with [Tutorial 5B](./README.md), sections 1–15. The purpose is to establish that you can access, inspect and explain your working environment before developing the full project. The sample web application is sufficient for this checkpoint.

Use Canvas for the exact demonstration time and practical arrangements. **Form your project group in Canvas immediately**; the deadline is Wednesday 4 November. **Also sign up separately for a design seminar in Canvas** on 16, 17 or 19 November. Those design seminars have six project groups per 90-minute session; they are separate from this environment demonstration.

## Prepare Before the Session

- Know your group number, members, assigned public IP and domain.
- Have SSH access to the group's VM and a browser ready to show the application.
- Complete the K3s, private kubeconfig, ingress and certificate setup in Tutorial 5B.
- Keep a short lab record with selected versions, DNS result, resource names, production HTTPS result, and unresolved issues.
- Prepare a diagram of `browser → domain/VM → Traefik → Service → Pod`. Explain the direction and protocol of each connection.
- Make sure every member can explain a part of the environment.

Keep `tls-demo` until the demonstration. If you already moved to Tutorial 7 or your application, show equivalent resources in their actual namespace. Do not create two Ingresses for the same hostname and `/` route just to reproduce example names.

The finished project, a separate monitoring stack and an advanced feature are not required at this checkpoint. The current numbered core assignment list is **REQ1–REQ26**; monitoring is supporting material rather than a separate numbered requirement.

## Demonstration Order

Aim for approximately eight minutes of prepared demonstration, leaving time for questions within the slot announced in Canvas. This is a suggested walkthrough, not a new fixed session duration.

| Step | Show | Explain |
| --- | --- | --- |
| Identify the environment | Group, domain, SSH terminal and remote hostname. | Which computer executes commands? What does SSH provide? |
| Show client access | Kubeconfig ownership/modes and selected context. | Why copy the root-owned configuration and select the private copy? |
| Inspect the cluster | Ready K3s node; Traefik and cert-manager components. | What is K3s? Which component did you install separately? |
| Follow a request | The actual Ingress, Service, Deployment and Pod. | How does a request for your hostname reach the container? |
| Demonstrate HTTPS | Normal verifying browser/client; production Certificate and issuer reference. | What does the certificate prove? Why is staging different? |
| Discuss operation | One diagnostic command and the renewal process. | What would the output tell you? What must work for renewal? |

Casper will rotate questions among members. Explain a command before interpreting its output. A screenshot can support discussion during a technical problem, but identify any live evidence still missing.

## Commands You Can Use as Evidence

These examples run **on the VM inside SSH**. Use your actual resource names if the sample has been replaced.

```bash
hostname
export KUBECONFIG="$HOME/.kube/config"
stat -c '%a %U:%G %n' "$HOME/.kube" "$KUBECONFIG"
kubectl config current-context
kubectl get nodes
```

- `hostname` identifies the remote computer.
- `export KUBECONFIG=...` selects the private copy for this shell's clients; it does not copy or create a configuration.
- `stat` displays permissions, owner/group and path without printing credentials. Expect directory mode `700`, file mode `600`, and ownership by the Ubuntu user.
- `current-context` reports the selected local context; it does not establish API reachability.
- `get nodes` contacts the API and shows node status. Explain the `Ready` result.

```bash
kubectl get pods -n kube-system
kubectl get pods -n cert-manager
kubectl get deployment,service,ingress -n tls-demo
kubectl get pods -n tls-demo -o wide
kubectl get certificate -n tls-demo
kubectl get clusterissuer letsencrypt-prod
```

`get` reads summaries; `-n` selects a namespace; `-o wide` adds details. The system namespace contains components such as Traefik. `cert-manager` contains the certificate controllers. The `tls-demo` resources describe the application. A cluster-scoped issuer has no application namespace. **A Ready issuer does not establish that the application certificate is issued or publicly served.**

```bash
kubectl describe ingress hello-world -n tls-demo
kubectl describe certificate hello-world-prod-tls -n tls-demo
kubectl get certificate hello-world-prod-tls -n tls-demo \
  -o jsonpath='{.spec.issuerRef.name}{"\n"}'
```

`describe` gives configuration, conditions and events. Follow the Ingress hostname, backend Service and TLS Secret name. The JSONPath expression prints the certificate's issuer; in this production example it should be `letsencrypt-prod`. A resource name containing `prod` is not evidence of its actual issuer. Keep kubeconfig contents, tokens, Secret values and private keys off screen.

**On a laptop**, open the public URL and inspect the served certificate. A terminal alternative is:

```bash
DOMAIN='group-07-m7011e-ltu.se'
curl --head "https://$DOMAIN"
```

Replace the example domain. `curl` makes an HTTPS request with normal certificate verification; `--head` asks for response headers. The sample supports this method; use a normal GET if your replacement application does not. A browser warning or `curl --insecure` does not demonstrate trusted production HTTPS. Inspect the hostname, validity and trust, and explain why the expected certificate is being served.

For an existing issue, choose a relevant read operation:

```bash
kubectl get events -n tls-demo --sort-by=.metadata.creationTimestamp
kubectl logs deployment/cert-manager -n cert-manager --tail=30
```

The first command orders namespace events by creation time. The second reads the latest controller log lines. Explain which hypothesis the output supports or rules out. Avoid projecting sensitive log contents. [Tutorial 5B's troubleshooting section](./README.md#15-troubleshooting-by-layer) explains the layers in more detail.

## Be Ready to Explain

1. What is a Kubernetes distribution, and what does K3s package?
2. What do SSH, kubectl, kubeconfig, Traefik and cert-manager each do?
3. Why does `127.0.0.1:6443` refer to a different machine after leaving SSH?
4. How do a Deployment, a Pod and a Kubernetes Service differ?
5. Which connection uses port 80 during issuance, and which uses 443 afterwards?
6. Why can a staging Certificate be Ready while a browser rejects it?
7. Where does TLS terminate in the sample? Is the next connection encrypted?
8. What must remain functional for certificate renewal?
9. Which failures can replicas on one VM tolerate? Why is this not VM-level HA?
10. Which diagnostic would you choose if DNS works but the application returns an error?

No destructive fault demonstration is required here. Controlled load and resilience experiments come later; see [scientific evaluation and test harnesses](../10-testing-ci/SCIENTIFIC-EVALUATION.md).

## Finish and Continue

Record demonstrated evidence, any gap and the next action agreed with Casper. This checkpoint is separate from the final team grade and individual oral examination.

Afterwards, follow [the cleanup instructions](./README.md#16-clean-up-the-demo-and-continue) when replacing the sample. Keep K3s, Traefik, cert-manager and the issuers. Continue to [Tutorial 6](../06-k8s-getting-started/README.md) for optional laptop access and [Tutorial 7](../07-k8s-helloworld/README.md) for Helm.
