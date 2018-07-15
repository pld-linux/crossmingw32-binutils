Summary:	Cross MinGW32 GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - MinGW32 binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - MinGW32 binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla MinGW32 - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - MinGW32 binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - MinGW32 binutils
Name:		crossmingw32-binutils
Version:	2.31
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.lz
# Source0-md5:	1ea8ddd13bd6fdcab1fe6cf377894476
Patch0:		binutils-libdir.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	lzip
BuildRequires:	perl-tools-pod
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		i386-mingw32
%define		arch		%{_prefix}/%{target}

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the MinGW32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains cross targeted binutils.

%description -l pl.UTF-8
crossmingw32 jest kompletnym systemem do kroskompilacji, pozwalającym
budować aplikacje MS Windows pod Linuksem używając bibliotek MinGW32.
System składa się z binutils, gcc z g++ i objc, libstdc++ - wszystkie
generujące kod dla platformy i386-mingw32, oraz z bibliotek w formacie
COFF.

Ten pakiet zawiera binutils generujące skrośnie binaria dla Win32.

%prep
%setup -q -n binutils-%{version}
%patch0 -p1

# file contains hacks for ac 2.64 only
%{__rm} config/override.m4
%{__sed} -i '/^m4_include(config\/override\.m4/d' configure.ac

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}

# non-standard regeneration (needed because of libdir patch)
# AM_BINUTILS_WARNINGS in bfd/warning.m4, ZW_GNU_GETTEXT_SISTER_DIR in config/gettext-sister.m4
for dir in gas bfd; do
	cd $dir || exit 1
	%{__aclocal} -I .. -I ../config -I ../bfd
	%{__automake} Makefile
	%{__automake} doc/Makefile
	%{__autoconf}
	cd ..
done

# We don't install libbfd (nor use shared binutils libraries) to avoid
# conflict with native binutils.

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-nls \
	--disable-shared \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL='$$s/install-sh -c' \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# not prefixed, keep infos only from native packages
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}

# "filesystem" for crossmingw32-* packages (move to crossmingw32-dirs?)
install -d $RPM_BUILD_ROOT%{arch}/lib/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
# mingw32 directory tree
%dir %{arch}
%dir %{arch}/lib
%dir %{arch}/lib/pkgconfig
%dir %{arch}/bin
# binutils files
%attr(755,root,root) %{arch}/bin/ar
%attr(755,root,root) %{arch}/bin/as
%attr(755,root,root) %{arch}/bin/dlltool
%attr(755,root,root) %{arch}/bin/ld
%attr(755,root,root) %{arch}/bin/ld.bfd
%attr(755,root,root) %{arch}/bin/nm
%attr(755,root,root) %{arch}/bin/objcopy
%attr(755,root,root) %{arch}/bin/objdump
%attr(755,root,root) %{arch}/bin/ranlib
%attr(755,root,root) %{arch}/bin/readelf
%attr(755,root,root) %{arch}/bin/strip
%{arch}/lib/ldscripts
%attr(755,root,root) %{_bindir}/%{target}-addr2line
%attr(755,root,root) %{_bindir}/%{target}-ar
%attr(755,root,root) %{_bindir}/%{target}-as
%attr(755,root,root) %{_bindir}/%{target}-c++filt
%attr(755,root,root) %{_bindir}/%{target}-dlltool
%attr(755,root,root) %{_bindir}/%{target}-dllwrap
%attr(755,root,root) %{_bindir}/%{target}-elfedit
%attr(755,root,root) %{_bindir}/%{target}-gprof
%attr(755,root,root) %{_bindir}/%{target}-ld
%attr(755,root,root) %{_bindir}/%{target}-ld.bfd
%attr(755,root,root) %{_bindir}/%{target}-nm
%attr(755,root,root) %{_bindir}/%{target}-objcopy
%attr(755,root,root) %{_bindir}/%{target}-objdump
%attr(755,root,root) %{_bindir}/%{target}-ranlib
%attr(755,root,root) %{_bindir}/%{target}-readelf
%attr(755,root,root) %{_bindir}/%{target}-size
%attr(755,root,root) %{_bindir}/%{target}-strings
%attr(755,root,root) %{_bindir}/%{target}-strip
%attr(755,root,root) %{_bindir}/%{target}-windmc
%attr(755,root,root) %{_bindir}/%{target}-windres
%{_mandir}/man1/%{target}-addr2line.1*
%{_mandir}/man1/%{target}-ar.1*
%{_mandir}/man1/%{target}-as.1*
%{_mandir}/man1/%{target}-c++filt.1*
%{_mandir}/man1/%{target}-dlltool.1*
%{_mandir}/man1/%{target}-elfedit.1*
%{_mandir}/man1/%{target}-gprof.1*
%{_mandir}/man1/%{target}-ld.1*
%{_mandir}/man1/%{target}-nm.1*
%{_mandir}/man1/%{target}-objcopy.1*
%{_mandir}/man1/%{target}-objdump.1*
%{_mandir}/man1/%{target}-ranlib.1*
%{_mandir}/man1/%{target}-readelf.1*
%{_mandir}/man1/%{target}-size.1*
%{_mandir}/man1/%{target}-strings.1*
%{_mandir}/man1/%{target}-strip.1*
%{_mandir}/man1/%{target}-windmc.1*
%{_mandir}/man1/%{target}-windres.1*
