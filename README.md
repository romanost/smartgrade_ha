# SmartGrade Home Assistant component #

Used to control Smart Grade devices

You must have the Smart Grade Docker running [https://github.com/romanost/smartgrade_docker](https://github.com/romanost/smartgrade_docker)

### Installation using HACS

1. Add `https://github.com/romanost/smartgrade_ha` as a custom repository
2. Click install under "Smart Grade"
3. Configure the integration and restart the Home Assistant


### Manual Installation

1. Download `smartgrade_ha.zip`
2. Unpack and copy the `custom_components/smartgrade_ha` folder into
   the `custom_components` folder directory of your Home Assistant.
3. Configure the integration and restart the Home Assistant


### Configuration
```yaml
hasmartgrade:
  host: 192.168.1.100
  port: 3000
  ssl: false
```