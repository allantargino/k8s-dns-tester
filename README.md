# Kubernetes DNS Tester

## Requirements

You will need to have:

* A Kubernetes cluster up and running.

And also to install:

* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Draft](https://github.com/azure/draft)
* [Helm](https://docs.helm.sh/using_helm/)

## Quickstart

### Application

Build the application:

```bash
draft up
```

This will create the application deployment and a service exposed as:
`http://prom-metric-prometheus-metrics:8000`

You can test the service using a simple `port-forward`:

```bash
export POD_NAME=$(kubectl get pods --namespace default -l "app=prom-metric-prometheus-metrics" -o jsonpath="{.items[0].metadata.name}")

kubectl --namespace default port-forward $POD_NAME 8000
```

In other terminal, you can use:

```bash
$ curl -s localhost:8000/metrics | grep ^dns.*total

dns_success_total 1274.0
dns_error_total 0.0
```

### Prometheus

Install Prometheus:

```bash
helm install stable/prometheus --name prometheus -f prom-values.yml
```

> In order to test the service and the configurations, `port-forward` to a local port, than explore Prometheus dashboard. Also, you can inspect its `ConfigMaps`.

### Grafana

Install Grafana:

```bash
helm install stable/grafana --name grafana
```

Get your 'admin' user password by running:
*(example outputed from helm installation)*

```bash
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

As soon as you enter the grafana dashboard, use the user `admin` and your password to login.

> You can change your Grafana endpoint to `LoadBalancer` type - so its easier to connect into it. Otherwise you can `port-forward` into it.

Then you add need to add Prometheus as a data source, using the url `http://prometheus-server`.

By the end, just create a dashboard/panel with the following queries into Prometheus:

```grafana
dns_success_total / (dns_success_total + dns_error_total)
```

```grafana
dns_error_total / (dns_success_total + dns_error_total)
```

> You can import `grafana.json` into your Grafana dashboard. Instructions can be found [here](http://docs.grafana.org/reference/export_import/#importing-a-dashboard).
