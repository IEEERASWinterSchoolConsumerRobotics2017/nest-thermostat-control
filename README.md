# nest-thermostat-control
This python script automates control of a nest thermostat by requesting temperatures from the [wearable-robot-controller-bridge.] (https://github.com/IEEERASWinterSchoolConsumerRobotics2017/wearable-robot-controller-bridge)
The desired set temperature is set in the bridge and read by this script and updated on the nest. Current temperature is also read from the nest and pushed to the bridge.
## Dependencies
This script runs on Python3 and relies on the [python-nest](https://pypi.python.org/pypi/python-nest) library to communicate with the nest thermostat.

Other, possibly already included, libraries required include:
* os
* sys
* socket
* threading
* math

## Usage
2 environment variables are needed, USERNAME and PASSWORD. These include your login info for [home.nest.com](https://home.nest.com). Set these with:
```bash
export USERNAME=user@example.com
export PASSWORD=SuperSecretPassword
```
Then run the script from this same terminal:
```bash
python3 nest-control.py
```
