SUDGT Deployment
=================
To setup a server from a backup
```
ansible-playbook setup-server.yml --extra-vars "DATE=2019-05-17"
```

To setup a server without a backup
```
ansible-playbook setup-server.yml
```

To restore an existing server from a variable
```
ansible-playbook restore.yml --extra-vars "DATE=2019-05-17"
```

To edit vault variables
```
ansible-vault edit group_vars/all --vault-password-file ~/.vault.txt
```
