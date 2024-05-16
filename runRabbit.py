import time
import subprocess
from HighLevelControls.Managers.LoggingManager import LoggingManager

#Start AVAHI to make sure it is working
subprocess.call(['sudo', 'systemctl','start', 'avahi-daemon.service'])
#Start Rabbitmq to make sure it is working
subprocess.call(['sudo', 'service', 'rabbitmq-server','start'])
#Make sure RabbitMQ has the proper settings
#subprocess.call(['sudo', './home/pi/classroom/SetupBroker.sh'])

subprocess.call(['sudo', 'rabbitmqctl', 'delete_user', ' guest'])
subprocess.call(['sudo', 'rabbitmqctl', 'delete_vhost', '/'])
subprocess.call(['sudo', 'rabbitmqctl', 'await_startup', '--timeout', '500'])
#configure.json must be placed in /var/lib/rabbitmq to be found by rabbitmqctl
subprocess.call(['sudo', 'rabbitmqctl', 'import_definitions', 'configure.json'])

time.sleep(2)

LoggingManager.log_info("runRabbit: Finished initial set up now importing RabbitMQ")

import HighLevelControls.RabbitMQ as mq
