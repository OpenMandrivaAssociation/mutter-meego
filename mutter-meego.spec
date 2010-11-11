%define panel_name	meego-panel
%define panel_major	0
%define panel_libname	%mklibname %{panel_name} %{panel_major}
%define panel_develname	%mklibname %{panel_name} -d

Name: mutter-meego
Summary: MeeGo Netbook plugin for Metacity Clutter, aka, Mutter
Group: Graphical desktop/Other 
Version: 0.76.10
License: GPLv2
URL: http://www.meego.com
Release: %mkrel 4
Source0: http://repo.meego.com/MeeGo/releases/1.1/netbook/repos/source/mutter-meego-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: startup-notification-devel
BuildRequires: libmesagl-devel
BuildRequires: meego-mutter-devel
BuildRequires: libgnome-menu-devel
BuildRequires: libgtk+2-devel
BuildRequires: libdbus-glib-devel
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: libclutter-gtk0.10-devel
BuildRequires: gnome-control-center-netbook-devel
Requires: gnome-menus
Requires: meego-mutter
Requires: %{panel_libname} = %{version}-%{release}
Obsoletes: mutter-moblin <= 0.43.2

%description
MeeGo Netbook plugin for Metacity Clutter, aka, Mutter

%package -n %{panel_libname}
Summary: MeeGo panel libraries
Group: System/Libraries

%description -n %{panel_libname}
MeeGo panel libraries

%package -n %{panel_develname}
Summary: Development libraries and headers for %{panel_name}
Group: Development/C
Requires: %{panel_libname} = %{version}-%{release}
Provides: %{panel_name}-devel

%description -n %{panel_develname}
Development environment for %{panel_name}

%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
	if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
		mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
	fi
done

rm -Rf %{buildroot}%{_sysconfdir}/gconf/schemas/mutter-meego.schemas
rm -Rf %{buildroot}%{_bindir}/meego-launch
rm -Rf %{buildroot}%{_bindir}/meego-toolbar-properties
rm -Rf %{buildroot}%{_includedir}/mutter-meego
rm -Rf %{buildroot}%{_libdir}/control-center-1/extensions/libmtp.la
rm -Rf %{buildroot}%{_libdir}/control-center-1/extensions/libmtp.so
rm -Rf %{buildroot}%{_libdir}/control-center-1/extensions/libsystray.la
rm -Rf %{buildroot}%{_libdir}/control-center-1/extensions/libsystray.so
rm -Rf %{buildroot}%{_libdir}/libmtp-common.la
rm -Rf %{buildroot}%{_libdir}/libmtp-common.so
rm -Rf %{buildroot}%{_libdir}/libmtp-common.so.0
rm -Rf %{buildroot}%{_libdir}/libmtp-common.so.0.0.0
rm -Rf %{buildroot}%{_libdir}/meego-app-launches-store
rm -Rf %{buildroot}%{_datadir}/applications
rm -Rf %{buildroot}%{_datadir}/gtk-doc

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NEWS AUTHORS README ChangeLog
%{_libdir}/mutter/plugins/*
%{_datadir}/mutter-meego/*
%{_datadir}/locale/*

%files -n %{panel_libname}
%defattr(-,root,root,-)
%{_libdir}/lib%{panel_name}.so.%{panel_major}*

%files -n %{panel_develname}
%defattr(-,root,root,-)
%dir %{_includedir}/lib%{panel_name}
%{_includedir}/lib%{panel_name}/*
%{_libdir}/lib%{panel_name}.la
%{_libdir}/lib%{panel_name}.so
%{_libdir}/pkgconfig/%{panel_name}.pc
