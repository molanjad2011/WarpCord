# WarpCord (Go Edition)

A simple GUI launcher for Discord that allows you to use a **SOCKS5 or HTTP proxy**.

> Because Discord doesn’t need to know your real location.

```
██╗    ██╗ █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██████╗ ██╗██████╗
██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██║██╔══██╗
██║ █╗ ██║███████║██████╔╝██████╔╝██║     ██║   ██║██████╔╝██║██║  ██║
██║███╗██║██╔══██║██╔══██╗██╔═══╝ ██║     ██║   ██║██╔══██╗██║██║  ██║
╚███╔███╔╝██║  ██║██║  ██║██║     ╚██████╗╚██████╔╝██║  ██║██║██████╔╝
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝
```

WarpCord is a lightweight launcher that runs Discord through a proxy.
No unnecessary dependencies, no extra bloat—just what you need.

---

## Why?

- Access Discord in regions where it is restricted
- Route Discord through Tor or other proxies
- Separate Discord traffic for privacy and security
- Lightweight and simple

---

## Installation

### Requirements

- Go 1.20+
- Fyne library

Install Fyne CLI:

```bash
go install fyne.io/fyne/v2/cmd/fyne@latest
```

### Build the project

```bash
git clone https://github.com/YOURUSERNAME/warpcord.git
cd warpcord
go build -o warpcord
```

### Run

```bash
./warpcord
```

---

## Usage

1. Open the app
2. Select your proxy type (SOCKS5, HTTP, or None)
3. Enter the IP address and port
4. Click **Warp Discord**
5. Discord will launch with the selected proxy

Settings are automatically saved at:

```
~/.config/warpcord/config.json
```

---

## Supported Proxy Types

| Type   | Description                          |
| ------ | ------------------------------------ |
| SOCKS5 | Suitable for Tor or advanced proxies |
| HTTP   | Suitable for standard HTTP proxies   |
| None   | Run Discord normally without a proxy |

---

## Configuration File

Located at:

```
~/.config/warpcord/config.json
```

Example:

```json
{
  "proxy_type": "SOCKS5",
  "ip": "127.0.0.1",
  "port": "9050"
}
```

---

## Discord Path

By default, Discord is assumed to be installed at:

```
/opt/discord/Discord
```

If your installation path is different, modify the `DiscordPath` variable in the code.

---

## How It Works

WarpCord sets the environment variables:

```
http_proxy
https_proxy
```

and passes the `--proxy-server` argument to Discord.
The configuration is also saved for future launches.

---

## Roadmap (Planned Features)

- Proxy authentication (username/password)
- Test proxy connection before launch
- Auto-detect Discord installation path
- Multiple proxy profiles

---

## Contributing

Pull requests and suggestions are welcome.
Focus: simplicity, readability, and reliability.

---

## License

**GPL-3.0** — free and open source.

---

## Credits

Built with Go and Fyne.
Designed for simplicity and lightweight proxy management for Discord.

---

**Summary:**
WarpCord is a minimal, functional proxy launcher for Discord. Easy to use and lightweight.
