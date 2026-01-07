package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

const (
	DiscordPath = "/usr/bin/vesktop"
	AppName     = "WarpCord"
)

var (
	ProxyTypes   = []string{"None", "SOCKS5", "HTTP"}
	ProxySchemes = []string{"", "socks5", "http"}
	ConfigDir    = filepath.Join(os.Getenv("HOME"), ".config", "warpcord")
	ConfigFile   = filepath.Join(ConfigDir, "config.json")
)

type ProxyConfig struct {
	ProxyType string `json:"proxy_type"`
	IP        string `json:"ip"`
	Port      string `json:"port"`
}

func LoadConfig() ProxyConfig {
	b, err := os.ReadFile(ConfigFile)
	if err != nil {
		return ProxyConfig{ProxyType: "None"}
	}
	var c ProxyConfig
	_ = json.Unmarshal(b, &c)
	return c
}

func (c ProxyConfig) Save() error {
	os.MkdirAll(ConfigDir, 0755)
	b, _ := json.MarshalIndent(c, "", "  ")
	return os.WriteFile(ConfigFile, b, 0644)
}

func (c ProxyConfig) Validate() error {
	if c.ProxyType == "None" {
		return nil
	}
	if c.IP == "" {
		return fmt.Errorf("IP address required")
	}
	p, err := strconv.Atoi(c.Port)
	if err != nil || p < 1 || p > 65535 {
		return fmt.Errorf("Port must be 1-65535")
	}
	return nil
}

func (c ProxyConfig) ProxyURL() string {
	if c.ProxyType == "None" {
		return ""
	}
	i := 0
	for idx, v := range ProxyTypes {
		if v == c.ProxyType {
			i = idx
		}
	}
	return fmt.Sprintf("%s://%s:%s", ProxySchemes[i], c.IP, c.Port)
}

func main() {
	cfg := LoadConfig()
	a := app.New()
	win := a.NewWindow(AppName)
	win.Resize(fyne.NewSize(380, 200))

	proxySelect := widget.NewSelect(ProxyTypes, nil)
	proxySelect.SetSelected(cfg.ProxyType)

	ipEntry := widget.NewEntry()
	ipEntry.SetPlaceHolder("127.0.0.1")
	ipEntry.SetText(cfg.IP)

	portEntry := widget.NewEntry()
	portEntry.SetPlaceHolder("8080")
	portEntry.SetText(cfg.Port)

	launchBtn := widget.NewButton("Warp Discord", func() {
		cfg.ProxyType = proxySelect.Selected
		cfg.IP = ipEntry.Text
		cfg.Port = portEntry.Text

		if err := cfg.Validate(); err != nil {
			dialog := widget.NewLabel(err.Error())
			win.SetContent(container.NewVBox(dialog))
			return
		}

		if err := cfg.Save(); err != nil {
			dialog := widget.NewLabel("Failed to save config")
			win.SetContent(container.NewVBox(dialog))
			return
		}

		cmd := exec.Command(DiscordPath)
		if url := cfg.ProxyURL(); url != "" {
			cmd.Env = append(os.Environ(),
				"http_proxy="+url,
				"https_proxy="+url,
			)
			cmd.Args = append(cmd.Args, "--proxy-server="+url)
		}

		_ = cmd.Start()
		a.Quit()
	})

	content := container.NewVBox(
		widget.NewLabel("Proxy Type:"),
		proxySelect,
		widget.NewLabel("IP Address:"),
		ipEntry,
		widget.NewLabel("Port:"),
		portEntry,
		launchBtn,
	)

	win.SetContent(content)
	win.ShowAndRun()
}
