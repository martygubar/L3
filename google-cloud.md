# Google Cloud Project: Lving Learning Laboratory

## Virtual Machine
### Create ssh key
ssh-keygen -t ed25519 -f ~/.ssh/google-compute

### ssh config entry
Host vmlivelearnlab
    HostName 35.239.150.107
    User marty_gubar
    IdentityFile /Users/marty/.ssh/google-compute
    UserKnownHostsFile=/Users/marty/.ssh/google_compute_known_hosts

### Create the VM
gcloud compute instances delete vmlivinglearninglab --zone=us-central1-a

gcloud compute instances create vmlivinglearninglab \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --metadata=ssh-keys="marty_gubar:$(cat ~/.ssh/google-compute.pub)"
