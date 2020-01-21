# Cloudflare Logsclient

## Input Configuration

* Run the following commands:
```mkdir -p  $SPLUNK_HOME/etc/apps/cloudflare-logsclient/{bin,local}```
* Copy the script and config file to $SPLUNK_HOME/etc/apps/cloudflare-logsclient/bin. 
Runnig the script from a Splunk scripted input may cause SSL issues, Add the script to be run from crontab by executing `crontab -e` and adding the following line:

```* * * * * /opt/splunk/etc/apps/cloudflare-logsclient/bin/cf_logsclient.py```

* Copy the `rotate-cloudflare.sh` file to `/etc/cron.hourly` so the file rotates and does not fill up the disk. Make sure the script is executable by running `chmod +x /etc/cron.hourly/rotate-cloudflare.sh`.

## Splunk Configuration
* Add this to `/opt/splunk/etc/apps/cloudflare-logsclient/local/inputs.conf` in the app:
```
[monitor:///var/log/cloudflare_logs/cloudflare.log*]
index = <your_index>
sourcetype = cloudflare
disabled = false
```
If you are runnig the script on a heavy forwarder, add this to `local/props.conf`, otherwise add them to the props/transforms to the Indexers:
```
[cloudflare]
LINE_BREAKER = \{
SHOULD_LINEMERGE = false
TRUNCATE = 0
TIME_PREFIX = EdgeStartTimestamp":
TIME_FORMAT = %s%3N
MAX_TIMESTAMP_LOOKAHEAD = 12
TZ = UTC
```
Since the file name is created with a timestamp in the name, you can have Splunk strip that date from the source by copying the `transforms.conf` file to the local directory, and adding `TRANSFORMS-remove_date_cloudflare = remove_date_cloudflare` to the `[cloudflare]` stanza in `local/props.conf` on the Heavy forwarder or Indexer.
