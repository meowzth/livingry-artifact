ssh-copy-id otlab@192.168.1.70

ansible -i ./inventory.ini all -m ping

ansible-playbook -i inventory.ini deploy.yml
