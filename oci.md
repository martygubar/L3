# Using Oracle Cloud

## Setup - install CLI
brew update && brew install oci-cli
oci setup config

## Object storage buckets
oci os bucket create --name landing --compartment-id ocid1.compartment.oc1..aaaaaaaaf57ct47qlvjak5tr5medtzegrx4sidmxszjp3slc6ipbjalxeg2a

oci os bucket create --name gold --compartment-id ocid1.compartment.oc1..aaaaaaaaf57ct47qlvjak5tr5medtzegrx4sidmxszjp3slc6ipbjalxeg2a

oci os bucket list --compartment-id ocid1.compartment.oc1..aaaaaaaaf57ct47qlvjak5tr5medtzegrx4sidmxszjp3slc6ipbjalxeg2a

oci os object bulk-upload \
  --bucket-name landing \
  --src-dir ./eBird \
  --include "*.csv" \
  --prefix observations/ebird/

oci os object bulk-upload \
  --bucket-name landing \
  --src-dir ./iNaturalist \
  --include "*.csv" \
  --prefix observations/inaturalist/

oci os object list \
  --bucket-name gold 

  oci os object bulk-delete --bucket-name landing
  oci os object bulk-delete --bucket-name gold
  

  ## ADB
  Auth Token: AFRqpqo5{i11A[6hcl]w

  ## Create always free vm
    oci compute image list --compartment-id $COMPARTMENT_OCID \
    --operating-system "Oracle Linux" \
    --operating-system-version "9" \
    --lifecycle-state AVAILABLE \
    --query 'data[*].{"Image Name":"display-name", OCID:id}' \
    --all --output table

  export AVAILABILITY_DOMAIN_OCID=wXNs:US-CHICAGO-1-AD-1
  export AVAILABILITY_DOMAIN_OCID=wXNs:US-CHICAGO-1-AD-2
  
  export COMPARTMENT_OCID=ocid1.compartment.oc1..aaaaaaaaf57ct47qlvjak5tr5medtzegrx4sidmxszjp3slc6ipbjalxeg2a
  export AVAILABILITY_DOMAIN_OCID=wXNs:US-CHICAGO-1-AD-1
  export IMAGE_OCID=ocid1.image.oc1.us-chicago-1.aaaaaaaasrbvw2qh25ewu3gg2div6bkwvqdi2oilwxirhic3qa5tzzxrcdwa
  export SUBNET_OCID=ocid1.subnet.oc1.us-chicago-1.aaaaaaaag3uubshsuybzj5c5p3loxipcwsaaoq4ovnnr326edkoe7ofhfaoq
  export PUBLIC_KEY=/Users/marty/.ssh/ssh-key.pub

  oci compute instance launch \
    --display-name vm-l3 \
    --availability-domain $AVAILABILITY_DOMAIN_OCID \
    --compartment-id $COMPARTMENT_OCID \
    --subnet-id $SUBNET_OCID \
    --image-id $IMAGE_OCID \
    --shape VM.Standard.A1.Flex \
    --shape-config '{"ocpus": 1, "memoryInGBs": 6}' \
    --ssh-authorized-keys-file $PUBLIC_KEY 
    
    



