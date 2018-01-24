#! /usr/bin/python
import yaml, json, sys, argparse, urllib2

parser = argparse.ArgumentParser(description='Update statefulset yaml with user-defined attributes.')
parser.add_argument('config_yaml', metavar="config_file_url", help='url to yaml file containing cockroachdb statefulset configuration')
parser.add_argument('--size',  dest="size_in_gb", type=int, help='Desired volume size in GiB')
parser.add_argument('--version-tag', dest="version_tag", help='CockroachDB Docker tag to use')
parser.add_argument('--locality', dest="locality", help='Locality arguments to use')

args = parser.parse_args()

#parse configuration file
configs = list(yaml.load_all(urllib2.urlopen(args.config_yaml)))

#update size in place
for config in configs:
    if config['kind'] == 'StatefulSet':
        if args.size_in_gb:
            config['spec']['volumeClaimTemplates'][0]['spec']['resources']['requests']['storage'] = str(args.size_in_gb) + 'Gi'

        if args.locality:
            for container in config['spec']['template']['spec']['containers']:
                if container['name'] == 'cockroachdb':
                    container['command'] = [
                        "/bin/bash",
                        "-ecx",
                        "exec /cockroach/cockroach start --logtostderr --insecure --host $(hostname -f) --locality=" +
                            args.locality +" --http-host 0.0.0.0 --join cockroachdb-0.cockroachdb,cockroachdb-1.cockroachdb,cockroachdb-2.cockroachdb --cache 25% --max-sql-memory 25%"
                    ]
                    break


        if args.version_tag:
            for container in config['spec']['template']['spec']['containers']:
                if container['name'] == 'cockroachdb':
                    container['image'] = args.version_tag
                    break

sys.stdout.write(yaml.dump_all(configs))


