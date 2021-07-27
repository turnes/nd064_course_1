# nd064_C1

# Docker

```
cd  project
docker build -t techtrends .
docker run --rm --name techtrends-flask -d -t -p 7111:3111 techtrends
curl 127.0.0.1:7111
curl 127.0.0.1:7111/about
curl 127.0.0.1:7111/healthz
curl -X POST -F 'title=Test Article' -F 'content=Here is the content' 127.0.0.1:7111/create
curl 127.0.0.1:7111/metrics
curl 127.0.0.1:7111
```


# K8S
```
cd project
vagrant up
vagrant ssh
# inside vm
sudo -i
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.20.9+k3s1 sh
kubectl get nodes
kubectl get all --all-namespaces
source <(kubectl completion bash)
# K8S declarative 
kubectl apply -f /vagrant/kubernetes/namespace.yaml
kubectl apply -f /vagrant/kubernetes/deploy.yaml
kubectl apply -f /vagrant/kubernetes/service.yaml
kubectl get all -n sandbox
kubectl delete -f /vagrant/kubernetes/
# K8S Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm ls --all-namespaces
helm install techtrends-prod /vagrant/helm --values=/vagrant/helm/values-prod.yaml
helm install techtrends-staging /vagrant/helm --values=/vagrant/helm/values-staging.yaml
helm install techtrends /vagrant/helm --values=/vagrant/helm/values.yaml
helm ls --all-namespaces
kubectl get all --all-namespaces
helm uninstall techtrends-prod techtrends-staging techtrends
# K8S ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f https://raw.githubusercontent.com/udacity/nd064_course_1/main/solutions/argocd/argocd-server-nodeport.yaml
kubectl get svc -n argocd
# access argo web 192.168.50.4:30007   user: admin  password: 
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
kubectl apply -f /vagrant/argocd/helm-techtrends-staging.yaml
kubectl apply -f /vagrant/argocd/helm-techtrends-prod.yaml
# sync application using argo web

```