### Muhammad Anzar Ahmad(24bcs10289)

![alt text](image.png)

### running

![](image-1.png)

### pending

![alt text](image-2.png)

### succeeded

![alt text](image-3.png)

### failed

![alt text](image-4.png)

### crashloop backoff

![alt text](image-5.png)

### imagepullbackoff

![alt text](image-6.png)

### PORT FORWARDING

![alt text](image-7.png)

![alt text](image-8.png)

### DEPLOYMENT

![alt text](image-9.png)

### TROUBLESHOOTING

![alt text](image-10.png)
![alt text](image-12.png)

### SELECTOR MISMATCH

![alt text](image-13.png)

### REPLICASET SCALING

![alt text](image-14.png)


## The Need for Kubernetes Services

- Pod IP addresses are temporary and can change whenever Pods are replaced, restarted, or scaled.

- A Service provides a stable way to access Pods and automatically sends traffic to matching healthy Pods.

## ClusterIP

- ClusterIP provides a stable internal IP for communication between applications inside the Kubernetes cluster.

- It is commonly used for communication between services such as frontend, backend, and database.

## NodePort

- NodePort exposes a service through a specific port on every node in the cluster.

- It is mainly useful for development, testing, and simple external access.

## LoadBalancer

- LoadBalancer exposes a service externally through a cloud provider's load balancer.

- It is commonly used for applications that need to receive traffic from outside the cluster.

## ExternalName

- ExternalName connects a Kubernetes Service to an external domain using DNS instead of routing traffic through Kubernetes Pods.

- It is useful when an application needs to communicate with an external API or service.

## Headless Service

- A Headless Service does not have a virtual IP and instead provides the direct IP addresses of the associated Pods.

- It is commonly used with StatefulSets and distributed applications that need to communicate with individual Pods.