podman build -t localhost/pokedex:latest .
podman tag localhost/pokedex:latest quay.io/purefield0/pokedex:latest
podman push quay.io/purefield0/pokedex:latest
oc delete pod -l app=pokedex
