# CockroachDB Clusters via AWS CloudFormation

This repo contains an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template for quickly spinning up multi-node CockroachDB clusters for development/test environments.

![CockroachDB CloudFormation Architecture](/images/architecture-diagram.png?raw=true)

The included template allows users to select the number of nodes, the cluster version, the EC2 instance type, and the amount of storage available to each node. For a small amount of security, the CockroachDB cluster is deployed in a virtual private cloud that restricts access to specific IP address ranges.

While the region in which the CloudFormation stack runs is configurable, for this version the CockroachDB cluster is deployed in a single availability zone. Since this configuration would not survive an availability zone failure, we would not recommend it for production deployments.

## Deploying a cluster
[Click here](http://amzn.to/2BuqJvQ) to deploy CockroachDB using this template.

After you log in, you'll have the option to name your stack.

![Template Header](/images/cloudformation-template.png?raw=true)

Next, scroll down and configure your security and cluster settings.
![Stack Paramaters](/images/cloudformation-params.png?raw=true)

Lastly, be sure to give the template permission to create the nested CockroachDB stack within the soon-to-be-created private subnet.
![Capabilities Approval](/images/cloudformation-capabilities.png?raw=true)

In 10-15 minutes, the CloudFormation stack will say "CREATE_COMPLETE" and the cluster will be ready to process requests.
![Completed Stack](/images/create-complete.png?raw=true)

When the stack is complete, you will see three outputs to get you started: a link to the web ui, a connection string to your CockroachDB cluster, and the command to SSH, via the bastion host, into your Kubernetes master node.
![Completed Stack](/images/cf-outputs.png?raw=true)

*If your stack times out before it completes, you could be running into an [AWS service limit](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).*


## Scaling an existing cluster
To scale an existing CockroachDB stack you need to adjust the AWS AutoScaling group size and the Kubernetes stateful set replica count.

First navigate to your Kubernetes stack (logical id: K8sStack) from your top-level VPC stack.

![Navigate to the nested template](/images/nested-stack.png?raw=true)

Then click the link to the AutoScaling group that hosts your Kubernetes nodes (logical id: K8sNodeGroup).

![Click Autoscaling Group](/images/navigate-to-as.png?raw=true)

Adjust the group size to your desired capacity. Note that AWS has limits on the maximun number of instances per region.

![Set desired nodesize](/images/update-as-group.png?raw=true)

SSH into your Kubernetes master node using the command from the "outputs" section of the template

![Get SSH Command](/images/ssh-command.png?raw=true)

Once you've SSHed into the master note, use `kubectl` to scale your CockroachDB cluster to match your AutoScaling Group size.

`kubectl scale statefulsets cockroachdb --replicas=10`

Watch the cluster rebalance in the Web UI

![Web UI Scaling Out](/images/scaleout-graphs.png?raw=true)

## Deleting a cluster
When you are finished using the cluster, you should delete it so AWS does not continue to charge you.

You can learn how to do that [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html).
