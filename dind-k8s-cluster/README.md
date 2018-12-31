# Quick deployment for development/tests with multi-nodes

```
wget https://cdn.rawgit.com/kubernetes-sigs/kubeadm-dind-cluster/master/fixed/dind-cluster-v1.11.sh
chmod +x dind-cluster-v1.11.sh
NUM_NODES=3 ./dind-cluster-v1.11.sh up
```
(can take some time due to the download of the images)

`alias k=~/.kubeadm-dind-cluster/kubectl`

`k get pods`
```
NAME                                  READY     STATUS    RESTARTS   AGE
kube-apiserver-kube-master            1/1       Running   1          13m
kube-controller-manager-kube-master   1/1       Running   1          11m
kube-scheduler-kube-master            1/1       Running   1          10m
```
