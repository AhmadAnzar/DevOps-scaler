# Kubernetes Deployment Strategies

Name: Anzar
Enrollment Number: 24BCS10289

This session covers Pods, Deployments, ReplicaSets, a DaemonSet, and four
common ways to release a new application version.

## 1. Rolling update

Folder: `01-rolling-update`

A rolling update replaces old Pods with new Pods little by little. The
application keeps serving traffic during the update.

```bash
kubectl apply -f deployment/deployment-v1.yaml
kubectl get pods
kubectl apply -f deployment/deployment-v2.yaml
kubectl rollout status deployment/yatri-backend
kubectl get pods
kubectl rollout history deployment/yatri-backend
```

The Deployment uses `RollingUpdate`, `maxSurge: 1`, and
`maxUnavailable: 0`, so Kubernetes keeps the requested replicas available
while changing the version.

## 2. Blue-Green deployment

Folder: `02-blue-green`

Blue is the current version and Green is the new version. Both versions can
run at the same time. Traffic is switched to Green only after it is ready.
This makes rollback simple: point traffic back to Blue.

```bash
kubectl apply -f 02-blue-green/deployment-blue.yaml
kubectl apply -f 02-blue-green/service-blue.yaml
kubectl apply -f 02-blue-green/deployment-green.yaml
kubectl apply -f 02-blue-green/service-green.yaml
kubectl get deployments,pods,services
```

## 3. Canary deployment

Folder: `03-canary`

A canary release sends a small amount of traffic to the new version first.
The stable version continues serving most users. If the canary works well,
it can be increased gradually.

```bash
kubectl apply -f 03-canary/deployment-stable.yaml
kubectl apply -f 03-canary/deployment-canary.yaml
kubectl apply -f 03-canary/service.yaml
kubectl get deployments,pods,services
```

The stable and canary Pods use the same application label, so the Service can
send traffic to both versions. Their replica counts control the rough traffic
share.

## 4. Recreate deployment

Folder: `04-recreate`

A recreate deployment stops the old Pods before starting the new Pods. There
is a short period with no application Pods, but it avoids running two
versions at the same time.

```bash
kubectl apply -f 04-recreate/deployment-v1.yaml
kubectl get pods
kubectl apply -f 04-recreate/deployment-v2.yaml
kubectl rollout status deployment/app-recreate
kubectl get pods
```

The Deployment uses the `Recreate` strategy, so the old version is removed
before the new version starts.

## Pod and DaemonSet files

The `pod/nginx-pod.yaml` file creates a basic Nginx Pod. The
`daemonset/node-agent-ds.yaml` file runs a small logging agent on each
eligible node.

```bash
kubectl apply -f pod/nginx-pod.yaml
kubectl apply -f daemonset/node-agent-ds.yaml
kubectl get pods -o wide
kubectl get daemonset
```

## Useful checks

```bash
kubectl get deployments
kubectl get replicasets
kubectl get pods
kubectl describe deployment DEPLOYMENT_NAME
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Conclusion

Rolling updates change versions gradually. Blue-Green keeps two complete
versions and switches traffic between them. Canary sends a small amount of
traffic to the new version first. Recreate stops the old version before
starting the new one.
