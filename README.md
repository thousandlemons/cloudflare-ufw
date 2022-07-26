# Cloudflare `ufw`

A simple script that helps you automatically configure `ufw` rules so that Cloudflare IP subnets are always allowed to access your web server on port 80 and 443.

It also supports removing all `ufw` rules that were previously configured for Cloudfalre by this script, in case you want to switch to other solutions and clean up your `ufw` rules.

## Dependencies

* [UncomplicatedFirewall](https://wiki.ubuntu.com/UncomplicatedFirewall) (i.e. `ufw`)
* [Python 3](https://www.python.org/)
* Optional but recommended: schedule with `cron`

## Getting started

Clone the repository and `cd` into it.

To configure the `ufw` rules, simply run:

```bash
sudo bash update.sh
```

If you're running this script for the first time, you'll see a long console output like this:

```text
Adding IP subnet 173.245.48.0/20...
Rule added
Adding IP subnet 103.21.244.0/22...
Rule added
====================================================
...
Skipping a lot of lines here since they are too long
...
====================================================
Adding IP subnet 2a06:98c0::/29...
Rule added (v6)
Adding IP subnet 2c0f:f248::/32...
Rule added (v6)
```

Note that a lot of lines in the middle are skipped since the full console output is too long.

To delete all previously generated and configured rules, simply run:

```bash
sudo bash delete.sh
```

## Schedule with `cron`

Since the scripts require the `sudo` priviledge to configure `ufw` rules, the easiest way is to add it to the root user's `cron` jobs.

You can edit the root user's `cron` jobs by:

```bash
sudo crontab -e
```

For example, if you want to automatically fetch Cloudflare's IP subnets and update your `ufw` rules every day at 5 am, you can append this to the root user's `cron` jobs:

```
# Update ufw to allow Cloudflare IP subnets
0 5 * * * sudo bash /path/to/cloudflare-ufw/update.sh
```

Please note that the default cron `PATH` is set to `/usr/bin:/bin`. If this `PATH` doesn't include any of the following commands, you'll have to manually configure cron's `PATH`:

* `mkdir`
* `echo`
* `ufw`
* `curl`
* `python3`
* `bash`

## Technical details

### How it works

Upon each run, `update.sh` will:

1. Execute `sudo ufw status` and save the console output to `tmp/ufw-status.txt` (relative path to the project root)
1. Fetch the latest Cloudflares IP subnets from:
	* https://www.cloudflare.com/ips-v4
	* https://www.cloudflare.com/ips-v6
1. Save the fetched IP subnets to `tmp/cloudflare-ips.txt`.
1. Run `_generate_bash_script.py` to generate a bash script which deletes outdated `ufw` rules and adds new ones by comparing the existing rules and the newly retrieved IP subnets.
1. Execute the `tmp/update_ufw_rules.sh` generated in the previous step.

The `delete.sh` script runs in a similar way.

### Reserved `ufw` comment

This script can only remove previously configured Cloudflare rules by recognizing the `# cloudflare` comment in the output of `ufw status`. Hence, it's recommended **not** to use the same comment manually or for other purposes. 

### Generate scripts, visually inspect, then manually run

The scripts (`update.sh` and `delete.sh`) don't remove the generated temp files under `tmp/` (relative path) after run. This is purposefully designed so that these files, espeically the automatically generated scripts, can be manually inspected and verified whenever necessary.

If you want to manually execute the generated script after visual inspection, you can comment out the last line in `update.sh` (or `delete.sh`) before running it. Then, visually inspect the content of the generated script `tmp/update_ufw_rules.sh` (or `tmp/delete_ufw_rules.sh`), and manually run it later.

```
...
# Run the generated script
# You can comment out this line then manually verify and run the generated script
bash "$UPDATE_UFW_RULES_SCRIPT"
```

## Example

When you run `update.sh` for the first time, the automatically generated `tmp/update_ufw_rules.sh` will have the following content:
 
 ```
echo "Adding IP subnet 173.245.48.0/20..."
ufw allow from 173.245.48.0/20 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 103.21.244.0/22..."
ufw allow from 103.21.244.0/22 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 103.22.200.0/22..."
ufw allow from 103.22.200.0/22 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 103.31.4.0/22..."
ufw allow from 103.31.4.0/22 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 141.101.64.0/18..."
ufw allow from 141.101.64.0/18 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 108.162.192.0/18..."
ufw allow from 108.162.192.0/18 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 190.93.240.0/20..."
ufw allow from 190.93.240.0/20 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 188.114.96.0/20..."
ufw allow from 188.114.96.0/20 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 197.234.240.0/22..."
ufw allow from 197.234.240.0/22 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 198.41.128.0/17..."
ufw allow from 198.41.128.0/17 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 162.158.0.0/15..."
ufw allow from 162.158.0.0/15 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 104.16.0.0/13..."
ufw allow from 104.16.0.0/13 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 104.24.0.0/14..."
ufw allow from 104.24.0.0/14 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 172.64.0.0/13..."
ufw allow from 172.64.0.0/13 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 131.0.72.0/22..."
ufw allow from 131.0.72.0/22 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2400:cb00::/32..."
ufw allow from 2400:cb00::/32 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2606:4700::/32..."
ufw allow from 2606:4700::/32 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2803:f800::/32..."
ufw allow from 2803:f800::/32 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2405:b500::/32..."
ufw allow from 2405:b500::/32 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2405:8100::/32..."
ufw allow from 2405:8100::/32 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2a06:98c0::/29..."
ufw allow from 2a06:98c0::/29 to any port 80,443 proto tcp comment "cloudflare"
echo "Adding IP subnet 2c0f:f248::/32..."
ufw allow from 2c0f:f248::/32 to any port 80,443 proto tcp comment "cloudflare"
 ```

By default, `update.sh` automatically executes the generated script above. Then, you should expect some console output like this:

```
Adding IP subnet 173.245.48.0/20...
Rule added
Adding IP subnet 103.21.244.0/22...
Rule added
Adding IP subnet 103.22.200.0/22...
Rule added
Adding IP subnet 103.31.4.0/22...
Rule added
Adding IP subnet 141.101.64.0/18...
Rule added
Adding IP subnet 108.162.192.0/18...
Rule added
Adding IP subnet 190.93.240.0/20...
Rule added
Adding IP subnet 188.114.96.0/20...
Rule added
Adding IP subnet 197.234.240.0/22...
Rule added
Adding IP subnet 198.41.128.0/17...
Rule added
Adding IP subnet 162.158.0.0/15...
Rule added
Adding IP subnet 104.16.0.0/13...
Rule added
Adding IP subnet 104.24.0.0/14...
Rule added
Adding IP subnet 172.64.0.0/13...
Rule added
Adding IP subnet 131.0.72.0/22...
Rule added
Adding IP subnet 2400:cb00::/32...
Rule added (v6)
Adding IP subnet 2606:4700::/32...
Rule added (v6)
Adding IP subnet 2803:f800::/32...
Rule added (v6)
Adding IP subnet 2405:b500::/32...
Rule added (v6)
Adding IP subnet 2405:8100::/32...
Rule added (v6)
Adding IP subnet 2a06:98c0::/29...
Rule added (v6)
Adding IP subnet 2c0f:f248::/32...
Rule added (v6)
```
Finally, can run `sudo ufw status` to verify the result. The generated rules should look like:

```
...
80,443/tcp                 ALLOW       173.245.48.0/20            # cloudflare
80,443/tcp                 ALLOW       103.21.244.0/22            # cloudflare
80,443/tcp                 ALLOW       103.22.200.0/22            # cloudflare
80,443/tcp                 ALLOW       103.31.4.0/22              # cloudflare
80,443/tcp                 ALLOW       141.101.64.0/18            # cloudflare
80,443/tcp                 ALLOW       108.162.192.0/18           # cloudflare
80,443/tcp                 ALLOW       190.93.240.0/20            # cloudflare
80,443/tcp                 ALLOW       188.114.96.0/20            # cloudflare
80,443/tcp                 ALLOW       197.234.240.0/22           # cloudflare
80,443/tcp                 ALLOW       198.41.128.0/17            # cloudflare
80,443/tcp                 ALLOW       162.158.0.0/15             # cloudflare
80,443/tcp                 ALLOW       104.16.0.0/13              # cloudflare
80,443/tcp                 ALLOW       104.24.0.0/14              # cloudflare
80,443/tcp                 ALLOW       172.64.0.0/13              # cloudflare
80,443/tcp                 ALLOW       131.0.72.0/22              # cloudflare
...
80,443/tcp                 ALLOW       2400:cb00::/32             # cloudflare
80,443/tcp                 ALLOW       2606:4700::/32             # cloudflare
80,443/tcp                 ALLOW       2803:f800::/32             # cloudflare
80,443/tcp                 ALLOW       2405:b500::/32             # cloudflare
80,443/tcp                 ALLOW       2405:8100::/32             # cloudflare
80,443/tcp                 ALLOW       2a06:98c0::/29             # cloudflare
80,443/tcp                 ALLOW       2c0f:f248::/32             # cloudflare
```

Now, you can also try `delete.sh`, and re-add these rules by running `update.sh` later.