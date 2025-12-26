# Maintainer: molanjad2011 <thus.is.zero.point@gmail.com>
pkgname=warpcord-go
pkgver=1.0.0
pkgrel=1
pkgdesc="A simple Go + Fyne launcher for Discord with SOCKS5/HTTP proxy support"
arch=('x86_64')
url="https://github.com/molanjad2011/WarpCord"
license=('GPL3')
depends=('gtk3' 'webkit2gtk')
makedepends=('go' 'git')      
source=()
noextract=()

build() {
    cd "$srcdir"
    go build -o warpcord warpcord.go
}
package() {
    cd "$srcdir"
    install -Dm755 warpcord "$pkgdir/usr/bin/warpcord"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}

