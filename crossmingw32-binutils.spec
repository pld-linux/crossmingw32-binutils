Summary:	Mingw32 GNU Binary Utility Development Utilities - binutils
Name:		crossmingw32-binutils
# could someone test this with new binutils?
%define binversion 2.10.0.18
%define version 990111
Version:	%{version}
Release:	3
License:	GPL
Group:		Development/Tools
Group(pl):	Programowanie/Narzêdzia
ExclusiveArch:	%{ix86}
Source0:	ftp://ftp.gnu.org/pub/gnu/binutils-%{binversion}.tar.gz
Patch0:		binutils-info.patch
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	/bin/bash
Requires:	crossmingw32-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define target i386-mingw32
%define target_platform i386-pc-mingw32
%define _prefix /usr
%define arch %{_prefix}/%{target}

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains cross targeted binutils.

%prep

%setup -q -T -c -a0
(cd binutils-%{binversion}
%patch -p1
)

%build

rm -rf $RPM_BUILD_ROOT

# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
(cd binutils-%{binversion}

# ldscripts won't be generated properly if SHELL is not bash...
%{?debug:CFLAGS="-g -O" LDFLAGS=""}%{!?debug:CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s"} \
CONFIG_SHELL="/bin/bash" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} tooldir=%{_prefix} EXEEXT="" all
)

%install

rm -rf $RPM_BUILD_ROOT
(cd binutils-%{binversion}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

)

# binutils 2.10 sets exeext to ".exe"

for fn in $RPM_BUILD_ROOT%{_bindir}/%target-*.exe $RPM_BUILD_ROOT%{arch}/bin/*.exe ; do
	mv -f $fn `echo $fn | sed s/\.exe\$//`
done

# check if rpm automation handles this correctly:
#gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/%{target}-*
#strip $RPM_BUILD_ROOT%{_bindir}/%{target}-*

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*

%clean

rm -rf $RPM_BUILD_ROOT
