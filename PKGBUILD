pkgbase=sync_my_photos
pkgname=('sync_my_photos')
pkgver=1.0
pkgrel=1
pkgdesc="sync_my_photos"
arch=('any')
url="github"
license=('GPL')
makedepends=('python')
depends=('python' 'python-flickrapi')
source=()
install='sync_my_photos.install'

pkgver() {
    python ../setup.py -V
}

check() {
    pushd ..
    python setup.py check
    popd
}

package() {
    pushd ..
    DONT_START=1 python setup.py install --root=$pkgdir
    popd
}

