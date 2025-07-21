%global debug_package %{nil}
%global git_commit %(echo $(git ls-remote https://github.com/openwall/john.git bleeding-jumbo | cut -c1-7))

Name:           john
Version:        1.9.0
Release:        1.git%{git_commit}%{?dist}
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
BuildRequires:  yacc
BuildRequires:  yasm gmp-devel
BuildRequires:  libpcap-devel
BuildRequires:  bzip2-devel
BuildRequires:  flex
BuildRequires:  gmp-devel
BuildRequires:  zlib-devel

# Optional dependencies for various formats
BuildRequires:  krb5-devel
BuildRequires:  libicu-devel
BuildRequires:  libgssglue-devel
BuildRequires:  libssh-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  openldap-devel
BuildRequires:  perl
BuildRequires:  python3-devel
BuildRequires:  rocm-smi-lib-devel
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
./configure --with-openssl --enable-ntlm-v2

# Compile the source code using all available CPU cores
make -j%{?_smp_mflags}

%install
# John the Ripper doesn't have a traditional 'make install'.
# All compiled files are placed in the 'run' directory.
# We will manually install them to the correct locations in the buildroot.

# Install the main binary
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 ../run/john %{buildroot}%{_bindir}/john

# Install the configuration file
install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 ../run/john.conf %{buildroot}%{_sysconfdir}/john.conf

# Create a data directory for all other helper scripts and files
install -d -m 755 %{buildroot}%{_datadir}/john
cp -r ../run/* %{buildroot}%{_datadir}/john/

# Remove the files we've already installed elsewhere to avoid duplication
rm -f %{buildroot}%{_datadir}/john/john
rm -f %{buildroot}%{_datadir}/john/john.conf

# Install the man page
install -d -m 755 %{buildroot}%{_mandir}/man8
install -m 644 ../doc/john.8 %{buildroot}%{_mandir}/man8/john.8

%files
%license ../doc/LICENSE
%doc ../doc/README.md ../doc/INSTALL
%{_bindir}/john
%config(noreplace) %{_sysconfdir}/john.conf
%{_datadir}/john/
%{_mandir}/man8/john.8.gz

%changelog
* Mon Jul 21 2025 Your Name <you@example.com> - 1.9.0-1.git%{git_commit}
- Initial RPM packaging for the bleeding-jumbo branch of John the Ripper.
