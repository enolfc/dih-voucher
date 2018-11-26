Expected secrets

```
apiVersion: v1
kind: Secret
metadata:
  name: dih-config 
  namespace: dih 
type: Opaque
stringData:
  dih_config.py: |-
    from datetime import timedelta

    SECRET_KEY = 'xxxx'
    CHECKIN_USER = 'yyyy'
    CHECKIN_PWD = 'gggg'
    VOUCHER_TIME = timedelta(months=3)
```

and

```
kubectl create secret generic --namespace dih dih \
--from-literal=checkin_client_secret=xxxxx \
--from-literal=checkin_client_id=yyyyy \
--from-literal=checkin_crypto=435yrtdh
```
