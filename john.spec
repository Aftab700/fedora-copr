%global debug_package %{nil}

Name:           john
Version:        1.9.0
Release:        2%{?dist}
Summary:        A fast password cracker

License:        GPL-2.0-or-later
URL:            https://www.openwall.com/john/
Source0:        https://github.com/openwall/john/archive/bleeding-jumbo.tar.gz#/john-bleeding-jumbo.tar.gz

# Build dependencies from the official INSTALL-FEDORA guide
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  git
BuildRequires:  which

# Core dependencies
BuildRequires:  openssl-devel
BuildRequires:  bison
BuildRequires:  yasm
BuildRequires:  libpcap-devel
BuildRequires:  bzip2-devel
BuildRequires:  flex
BuildRequires:  gmp-devel
BuildRequires:  zlib-devel

# Optional dependencies for various formats
BuildRequires:  krb5-devel
BuildRequires:  libicu-devel
BuildRequires:  libssh-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  openldap-devel
BuildRequires:  perl
BuildRequires:  python3-devel
BuildRequires:  p11-kit-devel
BuildRequires:  libkadm5

%description
John the Ripper is a fast password cracker, currently available for many
flavors of Unix, macOS, Windows, DOS, BeOS, and OpenVMS. Its primary
purpose is to detect weak Unix passwords. Besides several crypt(3) password
hash types most commonly found on various Unix systems, supported out of
the box are macOS, Kerberos/AFS and Windows LM hashes, plus many more,
with a lot of optional formats available.

This package is built from the "bleeding-jumbo" branch, which includes
community-enhanced features and support for more formats.

%prep
%autosetup -n john-bleeding-jumbo -p1

%build
# The build process happens inside the 'src' directory
cd src
./configure --with-openssl

# Compile the source code using all available CPU cores
make %{?_smp_mflags}

%install
# John the Ripper doesn't have a traditional 'make install'.
# All compiled files are placed in the 'run' directory.
# We will manually install them to the correct locations in the buildroot.

# Create all necessary directories first
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sysconfdir}
install -d -m 755 %{buildroot}%{_datadir}/john
install -d -m 755 %{buildroot}%{_mandir}/man8

# Install the main binary
install -m 755 run/john %{buildroot}%{_bindir}/john

# Install the configuration file
install -m 644 run/john.conf %{buildroot}%{_sysconfdir}/john.conf

# Install all other executable scripts and tools to /usr/bin
# so they are in the user's PATH.
for f in $(find run -maxdepth 1 -type f -executable); do
    # The main 'john' binary is already handled, so skip it here.
    if [[ $(basename $f) != "john" ]]; then
        install -m 755 $f %{buildroot}%{_bindir}/
    fi
done

# Install all non-executable files (wordlists, .chr files, etc.) to /usr/share/john
for f in $(find run -maxdepth 1 -type f ! -executable); do
    # The 'john.conf' file is already handled, so skip it here.
    if [[ $(basename $f) != "john.conf" ]]; then
        install -m 644 $f %{buildroot}%{_datadir}/john/
    fi
done

# Fix ambiguous shebangs to be explicit, handling trailing whitespace etc.
# The build system correctly handles scripts that already specify python2.
for SCRIPT in $(find %{buildroot}%{_bindir} -type f -name "*.py"); do
    #sed -i '1s|^#!\s*/usr/bin/env python\s*$|#!/usr/bin/python3|' "$SCRIPT"
    #sed -i '1s|^#!\s*/usr/bin/env python2\s*$|#!/usr/bin/python2|' "$SCRIPT"
    #sed -i '1s|^#!\s*/usr/bin/env python3\s*$|#!/usr/bin/python3|' "$SCRIPT"
    sed -i 's|/usr/bin/env |/usr/bin/|' "$SCRIPT"
done

for SCRIPT in $(find %{buildroot}%{_bindir} -type f -name "*.pl"); do
    #sed -i '1s|^#!\s*/usr/bin/env perl\s*$|#!/usr/bin/perl|' "$SCRIPT"
    sed -i 's|/usr/bin/env |/usr/bin/|' "$SCRIPT"
done

%files
%license doc/LICENSE
%doc doc/README.md doc/INSTALL
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_datadir}/john/
%{_mandir}/man8/john.8.gz

%changelog
* Tue Jul 22 2025 Your Name <you@example.com> - 1.9.0-5
- Final corrections for COPR build environment.
