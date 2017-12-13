# CockroachDB Clusters via AWS CloudFormation

This repo contains an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template for quickly spinning up multi-node CockroachDB clusters for development/test environments.

![CockroachDB CloudFormation Architecture](/images/architecture-diagram.png?raw=true)

The included template allows users to select the number of nodes, the cluster version, the EC2 instance type, and the amount of storage available to each node. For a small amount of security, the CockroachDB cluster is deployed in a virtual private cloud that restricts access to specific IP address ranges.

While the region in which the CloudFormation stack runs is configurable, the CockroachDB cluster is deployed in a single availability zone within that region. Since this configuration would not survive an availability zone failure, we would not recommend it for production deployments.

## Deploying a cluster
[Click here](http://amzn.to/2C5IFhv) to deploy CockroachDB using this template.

In 10-15 minutes, the CloudFormation stack will say "CREATE_COMPLETE" and the cluster will be ready to process requests. You will see three outputs to get you started: a link to the web ui, a connection string to your CockroachDB cluster, and the command to SSH -- via the bastion host -- into your Kubernetes master node.
![Completed Stack](/images/cf-outputs.png?raw=true)

*If your stack times out before it completes, you could be running into an [AWS service limit](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).*


## Scaling an existing cluster
To scale an existing CockroachDB stack you need to adjust the AWS AutoScaling group size and the Kubernetes stateful set replica count.

To do that, you need to navigate to your Kubernetes stack (logical id: K8sStack) from the `resources` section of the top-level VPC stack and select the Auto Scaling resource (logical id: K8sNodeGroup) that hosts your Kubernetes nodes.

From there, you can adjust the group size to your desired capacity. Note that AWS has limits on the maximum number of instances per region.

![Set desired nodesize](/images/update-as-group.png?raw=true)

SSH into your Kubernetes master node using the command from the "outputs" section of the template

![Get SSH Command](/images/ssh-command.png?raw=true)

Once you've SSHed into the master note, use `kubectl` to scale your CockroachDB cluster to match your Auto Scaling group size.

`kubectl scale statefulsets cockroachdb --replicas=10`

Watch the cluster rebalance in the Web UI

![Web UI Scaling Out](/images/scaleout-graphs.png?raw=true)

## Deleting a cluster
When you are finished using the cluster, you should delete it so AWS does not continue to charge you.

You can learn how to do that [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html).

## Testing

If you edit this template, you can run tests using [TaskCat](https://github.com/aws-quickstart/taskcat)

*This template was originally forked from [Heptio's Kuberenets AWS Quick Start](https://github.com/heptio/aws-quickstart)*
