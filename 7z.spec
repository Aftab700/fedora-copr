%global debug_package %{nil}

Name:           7zip
Version:        25.00
Release:        1%{?dist}
Summary:        File archiver with a high compression ratio

# Use standard SPDX identifiers for the license
License:        LGPL-2.1-or-later and BSD-3-Clause and UnRar
URL:            https://www.7-zip.org
Source0:        %{url}/a/7z%(tr -d . <<<"%{version}")-src.tar.xz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  sed

%description
7-Zip is a file archiver with a high compression ratio.
This package provides the command-line tool '7z'.

%prep
%autosetup -c -n %{name}-%{version}-src


%build
# The 7-Zip source requires a MASM-compatible assembler (asmc) for the x86_64 build.
# We clone and build it here first.
echo "Building asmc assembler..."
git clone https://github.com/nidud/asmc.git
cd asmc/source/asmc

# Patch the asmc makefile on-the-fly:
# 1. Disable Position-Independent Executable (PIE) to fix the linker error.
# 2. Remove the 'sudo' command from the 'install' target, as it's not allowed.
sed -i 's/-Wl,-pie/-Wl,-no-pie/' makefile
sed -i '/sudo install/d' makefile

# Compile asmc
make #%{?_smp_mflags}
cd ../../../

# Add the newly built assembler to the PATH for the main 7-Zip build
export PATH=%{buildroot}/../BUILD/%{name}-%{version}-src/asmc/bin:$PATH
echo "PATH is now: $PATH"

# Now, build 7-Zip using the correct makefile for GCC
echo "Building 7-Zip..."
cd CPP/7zip/Bundles/Alone2
# Use the GCC makefile, which will now find and use 'asmc' from the PATH
make %{?_smp_mflags} -f makefile.gcc


%install
# Install the compiled binary into the buildroot
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 CPP/7zip/Bundles/Alone2/b/g/7zz %{buildroot}%{_bindir}/7zz

# Rename the executable to the more common '7z'
mv %{buildroot}%{_bindir}/7zz %{buildroot}%{_bindir}/7z


%files
%license DOC/License.txt
%doc DOC/History.txt DOC/readme.txt
%{_bindir}/7z


%changelog
* Mon Jul 21 2025 Your Name <you@example.com> - 25.00-1
- Initial package for version 25.00
- Added build-time cloning and patching of 'asmc' to enable x86_64 compilation
