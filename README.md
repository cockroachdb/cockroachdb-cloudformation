# CockroachDB Clusters via AWS CloudFormation

This repo contains an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template for quickly spinning up multi-node CockroachDB clusters for development/test environments.

![CockroachDB CloudFormation Architecture](/images/architecture-diagram.png?raw=true)

The included template allows users to select the number of nodes, the cluster version, the EC2 instance type, and the amount of storage available to each node. For a small amount of security, the CockroachDB cluster is deployed in a virtual private cloud that restricts access to specific IP address ranges.

While the region in which the CloudFormation stack runs is configurable, the CockroachDB cluster is deployed in a single availability zone within that region. Since this configuration would not survive an availability zone failure, we would not recommend it for production deployments.

## Deploying a cluster
[Click here](https://amzn.to/2CZjJLZ) to deploy CockroachDB using this template.

You can lean more about this template by reading our [documentation](https://www.cockroachlabs.com/docs/stable/deploy-a-test-cluster.html) and [release blog](https://www.cockroachlabs.com/blog/cloud-formation-test-cluster-deployment/).

## Testing

If you edit this template, you can run tests using [TaskCat](https://github.com/aws-quickstart/taskcat)

To run tests

1. Edit the json files in the `ci` directory so the `KeyName` value references your key
1. Open `config.yml` and double check the regions in which the tests will run. Make sure a key with your provided name is in those regions (or edit the region config to point to regions that do contain your specified key)
1. Run `taskcat -c cockroachdb-cloudformation/ci/config.yml -p`
1. The output will be in the `taskcat_outputs` directory. Simply open the `index.html` file to see the results. 

*This template was originally forked from [Heptio's Kuberenets AWS Quick Start](https://github.com/heptio/aws-quickstart)*
