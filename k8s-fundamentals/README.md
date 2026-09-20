### Muhammad Anzar Ahmad (24bcs10289)

### basic minikube commands
![alt text](image.png)

```bash
minikube start
minikube status
kubectl cluster-info
kubectl get nodes -o wide
```

## Notes
### What is minikube
Minikube is a tool that lets you run a small Kubernetes cluster locally on your computer. It is mainly used for learning, development, and testing Kubernetes applications.

### What is kubernetes
Kubernetes is an open-source platform used to deploy, manage, and scale containerized applications. It automatically handles things like running containers, restarting failed Pods, and managing application replicas.

### What is a pod
A Pod is the smallest deployable Kubernetes object. It normally contains one main application container, although helper, sidecar and init containers are also possible.

### Namespaces
Namespaces separate groups of resources inside one cluster. A name only needs to be unique inside its namespace.