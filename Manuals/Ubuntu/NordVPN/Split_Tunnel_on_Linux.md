Setting this up on a remote VPS can be a bit of a tightrope walk. If you route all traffic through the VPN without specific exceptions, you'll effectively lock yourself out of SSH and your websites will stop responding because the server will try to "reply" to requests via the VPN interface instead of the public one.

To achieve this, you need to use the NordVPN CLI's built-in **allowlist** feature and ensure **split tunneling** (or policy-based routing) is handled correctly.

---

## Step 1: Allowlist your Local and Service Ports

The NordVPN app on Linux includes a feature to bypass the VPN for specific ports or subnets. Since you are on a remote server, **do this before connecting** to avoid losing SSH access.

1. **Allow SSH:** This ensures you don't lose access to your terminal.
```bash
nordvpn allowlist add port 22

```


2. **Allow Web Traffic:** This allows incoming traffic on standard web ports to bypass the VPN tunnel.
```bash
nordvpn allowlist add port 80
nordvpn allowlist add port 443

```


3. **Allow your Subnet:** Looking at your `ip route`, your gateway is `172.31.1.1`. You should allowlist that local network range so the server can still talk to its own gateway.
```bash
nordvpn allowlist add subnet 172.31.1.0/24

```



---

## Step 2: Configure NordVPN Settings

To ensure the VPN behaves correctly for a server environment, you should enable the "Kill Switch" (to prevent leaks) but ensure that routing is handled properly.

```bash
nordvpn set technology nordlynx
nordvpn set killswitch on

```

---

## Step 3: Handle the "Return Path" (Advanced Routing)

The biggest challenge is **Asymmetric Routing**. When a user hits your public IP (`46.224.30.4`), the packet enters via `eth0`. By default, once the VPN is up, the server tries to send the response back via `nordlynx`. The user’s browser will reject this because the IP addresses don't match.

NordVPN's CLI tries to handle some of this, but if your websites are still unreachable, you may need to create a specific routing table for traffic originating from your public IP.

### The "IP Rule" Fix

Run these commands to force traffic that *starts* from your public IP to always go back out through the physical gateway (`172.31.1.1`):

1. **Create a new routing table:**
```bash
echo "200 public_bypass" | sudo tee -a /etc/iproute2/rt_tables

```


2. **Add a default route to that table:**
```bash
ip route add default via 172.31.1.1 dev eth0 table public_bypass

```


3. **Add a rule to use that table for your public IP:**
```bash
ip rule add from 46.224.30.4 table public_bypass

```



---

## Step 4: Connect and Test

Now you can safely trigger the connection:

```bash
nordvpn connect

```

### How to Verify:

* **Test Outgoing:** Run `curl ifconfig.me`. It should show a NordVPN IP address.
* **Test Incoming:** From your **home computer**, try to access your website via the public IP or run `ssh chris@46.224.30.4`.

---

### Important Note on Persistence

The `ip rule` and `ip route` commands in Step 3 are **temporary** and will vanish after a reboot. If they work, you should add them to a post-up script in Netplan or a simple crontab entry:
`@reboot sleep 10 && ip rule add from 46.224.30.4 table public_bypass` (though Netplan is the "proper" Ubuntu way).

Would you like me to show you how to make those routing rules permanent in your Netplan configuration?
