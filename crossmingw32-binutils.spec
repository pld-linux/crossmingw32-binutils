Summary:	Mingw32 Binary Utility Development Utilities - GNU binutils
Summary(pl):	Zestaw narzêdzi mingw32 - GNU binutils
Name:		crossmingw32-binutils
Version:	2.11.90.0.8
Release:	1
License:	GPL
Group:		Development/Tools
Group(de):	Entwicklung/Werkzeuge
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
ExclusiveArch:	%{ix86}
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Patch0:		binutils-info.patch
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	/bin/bash
Requires:	crossmingw32-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		i386-mingw32
%define		arch		%{_prefix}/%{target}

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains cross targeted binutils.

%description -l pl
crossmingw32 jest kompletnym systemem do kroskompilacji, pozwalaj±cym
budowaæ aplikacje MS Windows pod Linuksem u¿ywaj±c bibliotek mingw32.
System sk³ada siê z binutils, gcc z g++ i objc, libstdc++ - wszystkie
generuj±ce kod dla platformy i386-mingw32, oraz z bibliotek w formacie
COFF.

Ten pakiet zawiera binutils generuj±ce binaria Win32.

%prep
%setup -q -n binutils-%{version}
%patch -p1

%build
rm -rf $RPM_BUILD_ROOT

# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
# [the same applies to binutils 2.10.1.0.4]

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} tooldir=%{_prefix} EXEEXT="" all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib/*
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*

%clean
rm -rf $RPM_BUILD_ROOT
