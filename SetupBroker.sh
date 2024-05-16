#sudo rabbitmqctl add_user admin bZa6N4ZJ94RdVmfFWqWmTrp5BkXBm1bZ6CoUxvJaPUT8CJlyjVqnvBZuqegR7wrQe31Y2NXRArGMrRed

#sudo rabbitmqctl set_user_tags admin administrator

#sudo rabbitmqctl add_vhost Broker

#sudo rabbitmqctl set_permissions -p Broker admin ".*" ".*" ".*"

#sudo rabbitmqctl set_topic_permissions -p Broker admin ".*" ".*" ".*"

sudo rabbitmqctl delete_user guest

sudo rabbitmqctl delete_vhost /

