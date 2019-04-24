# rig-sim-remote

> Basic python application to received rig-sim data readings via serial or socket connection

This version of `rig-sim-remote` is compatible with `rig-sim 0.6.0`

#### Installing dependencies

```bash
pipenv install
```

#### Configuration

Copy the `rig-sim.yaml-dist` file to `rig-sim.yaml` and adjust the **connections** section to match your configuration on **rig-sim**. Communication may be enabled via socket, serial, or both.

#### Running rig-sim-remote

```bash
python3 rig-sim-remote.py
```
