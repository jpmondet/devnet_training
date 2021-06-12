# Testing gitlab-ci jobs locally


```
docker run -d \
  --name gitlab-runner \
  --restart always \
  -v $PWD:$PWD \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

`docker exec -it -w $PWD gitlab-runner gitlab-runner exec docker testjob`


When the job is using dind to build an image, we must path the socket :

`docker exec -it -w $PWD gitlab-runner gitlab-runner exec docker --docker-volumes /var/run/docker.sock:/var/run/docker.sock testjob`

(yeah, huge inception)
