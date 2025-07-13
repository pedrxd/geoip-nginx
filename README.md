# GeoIP for NGINX

A tool that generates NGINX configuration files for IP-based access control based on countries. It allows you to easily 
create whitelist or blacklist configurations to allow or deny access to your web server based on the visitor's country 
of origin.

## Usage

You can download the pre-built binary directly from the releases page:

```bash
# Download the binary
wget https://github.com/pedrxd/geoip-nginx/releases/download/v0.1.0/geoip_linux_x86_64

# Make it executable
chmod +x geoip_linux_x86_64

# Run it
./geoip_linux_x86_64 --countries <es,pt,fr> [--output filename.conf] [--type whitelist|blacklist]
```

### Parameters

- `-c, --countries`: Required. A comma-separated list of country codes (e.g., "es,pt,fr")
- `-o, --output`: Optional. The output file name (default: "whitelist.conf" or "blacklist.conf" based on the type)
- `-t, --type`: Optional. The type of list to generate: "whitelist" (default) or "blacklist"


### Examples

Generate a whitelist for Spain and save it to the default file (whitelist.conf):

```bash
./geoip_linux_x86_64 --countries es
```

Generate a blacklist for Ireland and save it to a custom file:

```bash
./geoip_linux_x86_64 --countries ie --type blacklist --output block_ie.conf
```


## Using the Generated Configuration

Include the generated configuration file in your NGINX server block:

```nginx
server {
    # ...

    # Uncomment if required: 
    # allow 10.0.0.0/8;
    # allow 172.16.0.0/12;
    # allow 192.168.0.0/16;

    # Include the generated GeoIP configuration
    include /path/to/block_ie.conf;

    # ...
}
```

## Run from code

```bash
git clone https://github.com/yourusername/geoip.git
cd geoip
```

### Initialize with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. To initialize the project with uv:

```bash
# Create a virtual environment and install dependencies with uv sync
uv sync
```

### Usage
Same as using the binary

```bash
uv run main.py --countries <es,pt,fr> [--output filename.conf] [--type whitelist|blacklist]
```
