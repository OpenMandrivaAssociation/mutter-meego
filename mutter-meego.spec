Name: mutter-meego
Summary: MeeGo Netbook plugin for Metacity Clutter, aka, Mutter
Group: Graphical desktop/Other 
Version: 0.76.10
License: GPLv2
URL: https://www.meego.com
Release: %mkrel 5
Source0: http://repo.meego.com/MeeGo/releases/1.1/netbook/repos/source/mutter-meego-%{version}.tar.bz2
Requires: mx
Requires: gnome-menus
#Requires: meego-menus
Requires: matchbox-panel
Requires: mutter-meego-branding
Requires: meego-mutter
Requires: GConf2
BuildRequires: mx-devel >= 0.9.0
BuildRequires: startup-notification-devel
#BuildRequires: mutter-plugins
BuildRequires: libmesagl-devel
BuildRequires: meego-mutter-devel
BuildRequires: libgnome-menu-devel
BuildRequires: libgtk+2-devel
BuildRequires: libdbus-glib-devel
BuildRequires: libGConf2-devel
BuildRequires: libxscrnsaver-devel
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: libclutter-gtk0.10-devel
BuildRequires: gnome-control-center-netbook-devel
Obsoletes: mutter-moblin <= 0.43.2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
MeeGo Netbook plugin for Metacity Clutter, aka, Mutter

%package devel
Summary: Development libraries and headers for %{name}
Group: Development/C
Requires: %{name} = %{version}-%{release}

%description devel
Development environment for %{name}

%package doc
Summary: API reference for libmeego-panel
Group: Development/Libraries
Requires: gtk-doc

%description doc
API reference for libmeego-panel for use with DevHelp.

# Can't distribute this because we don't fulfill all requirements
# of the MeeGo Compliance Program
#
#%package branding-upstream
#Summary: Mutter-meego default theme files
#License: Restricted
#Group: System/Desktop
#Requires: %{name} = %{version}-%{release}
#Provides: mutter-meego-branding

%description branding-upstream
Default theme files for the Netbook UX Shell.


%prep
%setup -q

%build
%configure2_5x \
  --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*.desktop

%find_lang mutter-meego-netbook-plugin

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
  if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
    mv %{buildroot}/%{_datadir}/doc/$f \
      %{buildroot}/%{_datadir}/doc/%{name}-%{version}
  fi
done

rm %{buildroot}%{_libdir}/libmeego-panel.la
rm %{buildroot}%{_libdir}/libmtp-common.la


%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/mutter-meego.schemas \
    > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/mutter-meego.schemas \
    > /dev/null || :
fi

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/mutter-meego.schemas  > /dev/null || :

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f mutter-meego-netbook-plugin.lang
%defattr(-,root,root,-)
%doc COPYING NEWS AUTHORS README ChangeLog
%{_libdir}/lib*.so.*
%{_libdir}/mutter/plugins/meego-netbook*
%{_libdir}/control-center*
%dir %{_datadir}/mutter-meego
%dir %{_datadir}/mutter-meego/dbus-xml
%{_datadir}/mutter-meego/dbus-xml/*
%{_datadir}/applications/meego-toolbar-properties.desktop
%{_datadir}/applications/system-tray-properties.desktop
%{_sysconfdir}/gconf/schemas/mutter-meego.schemas
%{_libdir}/meego-app-launches-store
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/meego-panel

#%files branding-upstream
#%defattr(-,root,root,-)
#%dir %{_datadir}/mutter-meego/theme
#%{_datadir}/mutter-meego/theme/*
