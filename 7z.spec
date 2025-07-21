Name:           7zip
Version:        25.00
Release:        1%{?dist}
Summary:        7-Zip is a file archiver with a high compression ratio

License:        7-Zip is free software with open source. The most of the code is under the GNU LGPL license. Some parts of the code are under the BSD 3-clause License. Also there is unRAR license restriction for some parts of the code. Read 7-Zip License information at https://www.7-zip.org/license.txt
URL:            https://www.7-zip.org
Source0:        %{url}/a/7z%(tr -d . <<<"%version")-src.tar.xz

BuildRequires:  make, gcc, gcc-c++

%description

# TODO fix flags
%global debug_package %{nil}

%prep
%autosetup -c %{name}-%{version}

%build
# TODO needs masm for cmpl_gcc_x64.mak
%make_build \
    -C CPP/7zip/Bundles/Alone2 \
    -f ../../cmpl_gcc.mak

%install
install -D -m 755 \
	CPP/7zip/Bundles/Alone2/b/g/7zz \
	%{buildroot}%{_bindir}/7zz
mv %{buildroot}%{_bindir}/7zz %{buildroot}%{_bindir}/7z

%files
%{_bindir}/7z

%changelog
%(curl -sk https://www.7-zip.org/history.txt | sed -n '/25\.00/,/^[0-9]\{2\}\.[0-9]\{2\}/p' | sed '$d' | sed '$d')
