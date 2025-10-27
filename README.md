# WarpCord
A simple Tool for using Discord with Socks5/http proxy

> Because Discord doesn't need to know where you actually are.

```
██╗    ██╗ █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██████╗ ██╗██████╗ 
██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██║██╔══██╗
██║ █╗ ██║███████║██████╔╝██████╔╝██║     ██║   ██║██████╔╝██║██║  ██║
██║███╗██║██╔══██║██╔══██╗██╔═══╝ ██║     ██║   ██║██╔══██╗██║██║  ██║
╚███╔███╔╝██║  ██║██║  ██║██║     ╚██████╗╚██████╔╝██║  ██║██║██████╔╝
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ 
```

A stupidly simple GTK4 launcher that wraps Discord in a proxy. That's it. No bloat, no BS.

## Why?

- Your network admin is annoying
- You want to route Discord through Tor
- You're paranoid (valid)
- You live in a country that thinks blocking Discord is a good idea
- You just like proxies idk

## Install

**Arch (btw):**
```bash
sudo pacman -S python gtk4 libadwaita python-gobject
chmod +x warpcord.py && ./warpcord.py
```

**Other distros:** Figure it out, you got this.

## Use

1. Run it
2. Pick your proxy type
3. Enter IP and port
4. Click the big blue button
5. Discord warps through space-time (via your proxy)

Settings auto-save to `~/.config/warpcord/config.json`

## Supported Proxies

- SOCKS5 (the good one)
- HTTP (the okay one)
- None (why are you even here?)

## Features

- Modern GTK4/Adwaita UI that doesn't look like it's from 2003
- Actually remembers your settings
- Validates your input so you don't accidentally put "definitely.not.a.proxy" as your IP
- Clean Python code with type hints (because we're not savages)
- Zero dependencies beyond the obvious GTK stuff

## How it works

Sets `http_proxy` and `https_proxy` env vars + passes `--proxy-server` to Discord. Boom. Magic.

## Config

Lives at `~/.config/warpcord/config.json`:
```json
{
  "proxy_type": "SOCKS5",
  "ip": "127.0.0.1", 
  "port": "9050"
}
```

Edit manually if you're into that.

## Roadmap

Maybe I'll add:
- Proxy auth (username/password)
- Multiple profiles
- Testing proxy before launch
- Discord auto-detection for non-Arch peasants

Maybe I won't. We'll see.

## Known Issues

- Assumes Discord lives at `/opt/discord/Discord` (change `DISCORD_PATH` if yours is special)
- No proxy auth yet
- Won't make your crush like you back

## Contributing

PRs welcome. Keep it simple, keep it clean.

## License

GPL-3.0 - Free as in freedom

## Credits

Made with Python, GTK4, and spite towards geo-restrictions.

---

**tl;dr:** Proxy launcher for Discord. Works. That's all you need to know.
