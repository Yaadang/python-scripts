import boto3
import schedule

client = boto3.client('ec2')
resource = boto3.resource('ec2')

# resource.create_instances(ImageId='ami-02d8bad0a1da4b6fd', MinCount=1, MaxCount=1, InstanceType='t2.micro')
# client.describe_instances()

instances = resource.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['terminated']}])
for instance in instances:
    print(instance.id, instance.instance_type)


def check_instance_status():
    statuses = ec2_client.describe_instance_status()
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['']


schedule.every(5).minutes.do(check_instance_status())

while true:
    schedule.r