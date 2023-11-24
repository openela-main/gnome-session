%global _changelog_trimtime %(date +%s -d "1 year ago")

%define po_package gnome-session-3.0

%if 0%{?fedora}
%else
%global with_session_selector 1
%endif

Name: gnome-session
Version: 3.28.1
Release: 21%{?dist}
Summary: GNOME session manager

License: GPLv2+
URL: http://www.gnome.org
Source0: http://download.gnome.org/sources/gnome-session/3.28/%{name}-%{version}.tar.xz
Source1: gnome.desktop
Source2: gnome-xorg.desktop

Source3: com.redhat.Kiosk.Script.desktop

Source4: com.redhat.Kiosk.desktop
Source5: com.redhat.KioskWithKeyboard.desktop

Source6: com.redhat.Kiosk.WindowManager.desktop
Source7: com.redhat.KioskWithKeyboard.WindowManager.desktop
Source8: redhat-kiosk.json

Source9: redhat-kiosk.session
Source10: redhat-kiosk-with-keyboard.session

Source11: redhat-kiosk

Source12: 20-redhat-kiosk.conf

Source13: 50-redhat-kiosk.dconf
Source14: 50-redhat-kiosk.dconf.locks
Source15: redhat-kiosk.dconf.profile

Patch0: 0001-gnome-session-don-t-validate-shell-before-using-it.patch

# Blacklist NV30: https://bugzilla.redhat.com/show_bug.cgi?id=745202
Patch1: gnome-session-3.3.92-nv30.patch
Patch3: gnome-session-3.6.2-swrast.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=772421
Patch4: 0001-check-accelerated-gles-Use-eglGetPlatformDisplay-EXT.patch

Patch10001: 0001-session-selector-show-cursor-explicitly.patch

# Downstream patch to provide better grub integration
# https://bugzilla.redhat.com/show_bug.cgi?id=1914925
Patch20001: 0001-Fedora-Set-grub-boot-flags-on-shutdown-reboot.patch

# Make some debug spew only show up if debugging is enabled
# https://bugzilla.redhat.com/show_bug.cgi?id=1877997
Patch30001: 0001-main-only-log-check-accelerated-errors-when-debuggin.patch

# Allow user to override language settings
# https://bugzilla.redhat.com/show_bug.cgi?id=2170474
Patch40001: 0001-gnome-session-avoid-setting-LC_-unless-LANG-and-regi.patch

BuildRequires: meson
BuildRequires: gcc
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(gnome-desktop-3.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xtrans)
BuildRequires: pkgconfig(xtst)

BuildRequires: gettext
BuildRequires: intltool
BuildRequires: xmlto
BuildRequires: /usr/bin/xsltproc
BuildRequires: python3-devel

# an artificial requires to make sure we get dconf, for now
Requires: dconf

Requires: system-logos
Requires: system-backgrounds
# Needed for gnome-settings-daemon
Requires: control-center-filesystem

Requires: gsettings-desktop-schemas >= 0.1.7

# pull in dbus-x11, see bug 209924
Requires: dbus-x11

Conflicts: gnome-settings-daemon < 3.27.90

%description
gnome-session manages a GNOME desktop or GDM login session. It starts up
the other core GNOME components and handles logout and saving the session.

%package xsession
Summary: Desktop file for gnome-session
Requires: %{name}%{?_isa} = %{version}-%{release}

%description xsession
Desktop file to add GNOME to display manager session menu.

%package wayland-session
Summary: Desktop file for wayland based gnome session
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: xorg-x11-server-Xwayland%{?_isa}

%description wayland-session
Desktop file to add GNOME on wayland to display manager session menu.

%package kiosk-session
Summary: Desktop file for mutter based kiosk session
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mutter
Recommends: gedit
Recommends: gnome-terminal
Recommends: gnome-control-center

%description kiosk-session
Desktop file to add basic session used for setting up kiosk applications.

%prep
%autosetup -p1

%build
%meson                                                          \
%if 0%{?with_session_selector}
           -Dsession_selector=true                              \
%endif
           -Dsystemd=true                                       \
           -Dsystemd_journal=true
%meson_build

%install
%meson_install

# Rename GNOME to Standard
cp $RPM_SOURCE_DIR/gnome.desktop $RPM_BUILD_ROOT%{_datadir}/wayland-sessions
cp $RPM_SOURCE_DIR/gnome.desktop $RPM_BUILD_ROOT%{_datadir}/wayland-sessions/gnome-wayland.desktop
cp $RPM_SOURCE_DIR/gnome-xorg.desktop $RPM_BUILD_ROOT%{_datadir}/xsessions
cp $RPM_SOURCE_DIR/gnome-xorg.desktop $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

install -D $RPM_SOURCE_DIR/com.redhat.Kiosk.Script.desktop -t $RPM_BUILD_ROOT%{_datadir}/applications

install -D $RPM_SOURCE_DIR/com.redhat.Kiosk.WindowManager.desktop -t $RPM_BUILD_ROOT/%{_datadir}/applications
install -D $RPM_SOURCE_DIR/com.redhat.KioskWithKeyboard.WindowManager.desktop -t $RPM_BUILD_ROOT/%{_datadir}/applications

install -D $RPM_SOURCE_DIR/com.redhat.Kiosk.desktop -t $RPM_BUILD_ROOT%{_datadir}/xsessions
install -D $RPM_SOURCE_DIR/com.redhat.KioskWithKeyboard.desktop -t $RPM_BUILD_ROOT%{_datadir}/xsessions

install -D $RPM_SOURCE_DIR/redhat-kiosk.json -t $RPM_BUILD_ROOT%{_datadir}/gnome-shell/modes

install -D $RPM_SOURCE_DIR/redhat-kiosk.session -t $RPM_BUILD_ROOT%{_datadir}/gnome-session/sessions
install -D $RPM_SOURCE_DIR/redhat-kiosk-with-keyboard.session -t $RPM_BUILD_ROOT%{_datadir}/gnome-session/sessions

install -D $RPM_SOURCE_DIR/redhat-kiosk -t $RPM_BUILD_ROOT%{_bindir}

install -D $RPM_SOURCE_DIR/20-redhat-kiosk.conf -t $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d

install -D $RPM_SOURCE_DIR/50-redhat-kiosk.dconf $RPM_BUILD_ROOT%{_sysconfdir}/dconf/db/redhatkiosk.d/50-redhat-kiosk
install -D $RPM_SOURCE_DIR/50-redhat-kiosk.dconf.locks $RPM_BUILD_ROOT%{_sysconfdir}/dconf/db/redhatkiosk.d/locks/50-redhat-kiosk
install -D $RPM_SOURCE_DIR/redhat-kiosk.dconf.profile $RPM_BUILD_ROOT%{_sysconfdir}/dconf/profile/redhatkiosk

install -D $RPM_SOURCE_DIR/20-redhat-kiosk.conf -t $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d

%find_lang %{po_package}

%ldconfig_scriptlets

%posttrans

# These files weren't packaged correctly in gnome-session-3.28.1-19.el8 so manually prune them
rmdir %{_sysconfdir}/dconf/db/redhat-kiosk.d/locks 2> /dev/null || :
rmdir %{_sysconfdir}/dconf/db/redhat-kiosk.d 2> /dev/null || :
rm -f %{_sysconfdir}/dconf/db/redhat-kiosk 2> /dev/null || :

dconf update

%files xsession
%{_datadir}/xsessions/*
%exclude %{_datadir}/xsessions/com.redhat.Kiosk.desktop

%files wayland-session
%{_datadir}/wayland-sessions/*

%files kiosk-session
%dir %{_sysconfdir}/dconf/db/redhatkiosk.d/locks
%dir %{_sysconfdir}/dconf/db/redhatkiosk.d
%ghost %{_sysconfdir}/dconf/db/redhatkiosk
%{_sysconfdir}/dconf/db/redhatkiosk.d/50-redhat-kiosk
%{_sysconfdir}/dconf/db/redhatkiosk.d/locks/50-redhat-kiosk
%{_sysconfdir}/dconf/profile/redhatkiosk
%{_datadir}/applications/com.redhat.Kiosk.Script.desktop
%{_datadir}/applications/com.redhat.Kiosk.WindowManager.desktop
%{_datadir}/applications/com.redhat.KioskWithKeyboard.WindowManager.desktop
%{_datadir}/gnome-shell/modes/redhat-kiosk.json
%{_datadir}/xsessions/com.redhat.Kiosk.desktop
%{_datadir}/xsessions/com.redhat.KioskWithKeyboard.desktop
%{_datadir}/gnome-session/sessions/redhat-kiosk.session
%{_datadir}/gnome-session/sessions/redhat-kiosk-with-keyboard.session
%{_datadir}/X11/xorg.conf.d/20-redhat-kiosk.conf
%{_bindir}/redhat-kiosk

%files -f %{po_package}.lang
%doc AUTHORS NEWS README
%license COPYING
%doc %{_mandir}/man*/*
%{_bindir}/*
%{_libexecdir}/gnome-session-binary
%{_libexecdir}/gnome-session-check-accelerated
%{_libexecdir}/gnome-session-check-accelerated-gl-helper
%{_libexecdir}/gnome-session-check-accelerated-gles-helper
%{_libexecdir}/gnome-session-failed
%{_datadir}/gnome-session/
%{_datadir}/doc/gnome-session/dbus/gnome-session.html
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml

%changelog
* Wed May 31 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-21
- Allow users to override language settings in environment
  Resolves: #2170474

* Wed Mar 01 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-20
- Work around dconf log spew by renaming dconf profile
  Related: 2070976
  Resolves: #2174414

* Tue Feb 28 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-19
- Another fix
  Related: #2070976

* Tue Feb 28 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-18
- Fix issue introduced in last build
  Related: #2070976

* Tue Feb 28 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-17
- Don't force kiosk profile for user in non-kiosk sessions
  after the user has been used for a kiosk session once
  Related: #2070976

* Tue Feb 28 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-16
- Fix glitch where enabling on-screen keyboard requires initial
  reboot
  Related: #2070976

* Mon Feb 27 2023 Ray Strode <rstrode@redhat.com> - 3.28.1-15
- Add new shell based variant of kiosk mode that supports
  on-screen keyboard
  Resolves: #2070976

* Tue Dec 21 2021 Ray Strode <rstrode@redhat.com> - 3.28.1-14
- Make some debug spew only show up if debugging is enabled
  Resolves: #1877997

* Mon Jul 26 2021 Ray Strode <rstrode@redhat.com> - 3.28.1-13
- Add patch to tell grub boot was successful when user is
  able to explicitly request shutdown/reboot.
  Resolves: #1914925

* Tue Jul 20 2021 Ray Strode <rstrode@redhat.com> - 3.28.1-12
- Introduce gnome-wayland session to allow users that use
  Xorg on the login screen to try wayland for the user session.
  Related: #1962211

* Fri Jun 04 2021 Ray Strode <rstrode@redhat.com> - 3.28.1-11
- Exclude kiosk-session from xsession subpackage
- Disable VT switching when kiosk-session is installed
  Related: #1955754

* Mon Jun 29 2020 Ray Strode <rstrode@redhat.com> - 3.28.1-10
- Show cursor explicitly from session selector
  Resolves: #1624430

* Tue May 19 2020 Ray Strode <rstrode@redhat.com> - 3.28.1-9
- Add kiosk-session subpackage to help users set up RHEL for
  kiosk/point-of-sale use.
  Resolves: #1739556

* Wed Nov 20 2019 Tomas Pelka <tpelka@redhat.com> - 3.28.1-8
- rebuild and version bump to avoid future conflict with z-stream version
  Resolves: #1745147

* Tue Nov 19 2019 Ray Strode <rstrode@redhat.com> - 3.28.1-7
- make /sbin/nologin fail on wayland
  Resolves: #1745147

* Mon Jan 14 2019 Ray Strode <rstrode@redhat.com> - 3.28.1-6
- Update desktop file names
  Related: #1647713

* Thu Nov 01 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-5
- Drop usermode dependency, it's vestigial
  Resolves: #1643696

* Fri Sep 07 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-4
- Require system-backgrounds
  Related: #1626388

* Wed Aug 22 2018  Ray Strode <rstrode@redhat.com> - 3.28.1-3
- Rename GNOME to Standard
  Related: #1612915

* Mon Aug 13 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-2
- BuildRequire python3 binary
  Resolves: #1615527

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Fri Mar 02 2018 Kalev Lember <klember@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Tue Feb 13 2018 Ray Strode <rstrode@redhat.com> - 3.27.90.1-1
- Update to 3.27.90.1

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.4-2
- Rebuild against newer gnome-desktop3 package

* Fri Feb 09 2018 Bastien Nocera <bnocera@redhat.com> - 3.27.4-1
- Update to 3.27.4
- Use meson as build system
- Adjust required session components for gnome-settings-daemon 3.27.90

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.1-3
- Switch to %%ldconfig_scriptlets

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.1-2
- Remove obsolete scriptlets

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Fri Sep 08 2017 Kalev Lember <klember@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Bastien Nocera <bnocera@redhat.com> - 3.25.3-1
+ gnome-session-3.25.3-1
- Update to 3.25.3

* Wed Jun 21 2017 Ray Strode <rstrode@redhat.com> - 3.24.1-2
- Kill bus clients at log out
  Resolves: #1340203

- Address crash in fail whale
  Related: #1384508

* Wed Apr 12 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Tue Feb 28 2017 Richard Hughes <rhughes@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 3.23.4.1-1
- Update to 3.23.4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 11 2016 Adam Jackson <ajax@redhat.com> - 3.23.2-2
- Prefer eglGetPlatformDisplay to eglGetDisplay

* Tue Oct 11 2016 Bastien Nocera <bnocera@redhat.com> - 3.23.2-1
+ gnome-session-3.23.2-1
- Update to 3.23.2

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Don't set group tags

* Fri Aug 19 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Tue Mar 15 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Mon Mar 07 2016 Kalev Lember <klember@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Kalev Lember <klember@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Wed Nov 11 2015 Ray Strode <rstrode@redhat.com> 3.19.2-0.1.20151111git858812a7
- Add GNOME on Xorg session

* Tue Nov 10 2015 Ray Strode <rstrode@redhat.com> 3.19.2-0.1.20151110git9bbaf36d
- Update to git snapshot

* Fri Nov 06 2015 Ray Strode <rstrode@redhat.com> 3.18.1.2-2
- Add patch to make crash logging more obvious
  Related: gnome#757571

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.1.2-1
- Update to 3.18.1.2

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.1.1-1
- Update to 3.18.1.1

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Thu Sep 17 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92
- Use make_install macro

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.16.0-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Wed Mar 18 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Remove patch fuzz 2 and drop two upstreamed patches
- Tighten deps with the _isa macro

* Sat Mar 07 2015 Bastien Nocera <bnocera@redhat.com> 3.15.90-2
- Fix SessionIsActive property thereby fixing screens not going to sleep
- Disable GConf autostart support

* Thu Feb 19 2015 David King <amigadave@amigadave.com> - 3.15.90-1
- Update to 3.15.90

* Thu Jan 29 2015 David King <amigadave@amigadave.com> - 3.15.4-1
- Update to 3.15.4
- Use license macro for COPYING
- Use pkgconfig for BuildRequires

* Mon Jan 05 2015 Ray Strode <rstrode@redhat.com> 3.15.3-2
- Fix crasher
  Resolves: #1176413

* Fri Dec 19 2014 Richard Hughes <rhughes@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Sat Nov 01 2014 Richard Hughes <rhughes@redhat.com> - 3.14.0-2
- Fix compile on RHEL

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Ray Strode <rstrode@redhat.com> 3.13.3-1
- Update to 3.13.3
- Fix classic mode
  Resolves: #1120283

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-2
- Pull in xorg-x11-server-Xwayland for the wayland session

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Tue Apr 15 2014 Ray Strode <rstrode@redhat.com> 3.12.0-3
- Actually move wayland session to subpackage, instead of
  copy it to subpackage

* Tue Apr 08 2014 Ray Strode <rstrode@redhat.com> - 3.12.0-2
- Move wayland session to a subpackage

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-2
- Rebuilt for gnome-desktop soname bump

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Sun Nov 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.11.1-1
- Update to 3.11.1

* Fri Nov 01 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.1-2
- Backport patch for UPower 1.0 support

* Mon Oct 14 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90
- Switch to unversioned docdirs (#993784)

* Sat Aug 10 2013 Ray Strode <rstrode@redhat.com> 3.9.5-2
- Remove vendor from desktop-file-install

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Matthias Clasen <mclasne@redhat.com> - 3.8.2.1-2
- Trim %%changelog

* Wed May 15 2013 Matthias Clasen <mclasne@redhat.com> - 3.8.2.1-1
- Update to 3.8.2.1
- Conditionally build session selector

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Apr 30 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-2
- Use the upstream xsession desktop file
- Drop the fallback mode authentication agent autostart file

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Thu Apr 11 2013 Adam Jackson <ajax@redhat.com> 3.8.0-2
- gnome-session-3.6.2-swrast.patch: Allow running on the classic software
  renderer.  No effect on arches where we build llvmpipe, but on ppc/s390
  classic swrast is marginally less painful than softpipe.

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Sun Feb 24 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.90-2
- Drop obsolete requires (polkit-gnome, polkit-desktop-policy,
  notification-daemon)

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3
- Drop the upstreamed llvmpipe patch
- Adjust buildrequires

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Thu Oct 18 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.1-2
- Set XDG_MENU_PREFIX to pick the correct menu layout in
  gnome-shell and alacarte

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Dropped upstreamed systemd patch

* Thu Apr  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.0-2
- Fix a looping PolicyKit dialog on shutdown

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Thu Mar 22 2012 Adam Williamson <awilliam@redhat.com> - 3.3.92-2
- blacklist NV30 family until RH #745202 is resolved

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Thu Feb  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-2
- Fix a bug in the new system interface registration

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5
- Use systemd for session tracking

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> 3.3.3-1
- Update to 3.3.3

* Tue Dec 13 2011 Adam Jackson <ajax@redhat.com> 3.3.2-2
- gnome-session-3.3.2-radeon.patch: Blacklist pre-R300 radeons (#758422)

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> 3.3.2-1
- Update to 3.3.2

* Thu Nov 03 2011 Adam Jackson <ajax@redhat.com> 3.3.1-2
- gnome-session-3.3.1-llvmpipe.patch: Don't consider llvmpipe unsupported.

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> 3.1.92-1
- Update to 3.1.92

* Fri Sep  9 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91-3
- Some fixes to make gdm fallback mode login work

* Thu Sep  8 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91-2
- Drop GConf2-gtk dep

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90

* Wed Aug 17 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed Apr 27 2011 Owen Taylor <otaylor@redhat.com> - 3.0.1-2
- Add a quick-and-dirty blacklist for Radeon R100, R200, Intel 8xx

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.94-1
- Update to 2.91.94

* Wed Mar 23 2011 Ray Strode <rstrode@redhat.com> 2.91.93-1
- Update to 2.91.93

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update to 2.91.92

* Wed Mar  9 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91.3-1
- Update to 2.91.91.3

* Wed Mar  9 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91.2-1
- Update to 2.91.91.2

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-2
- Fix the check-accel utility exit status

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-1
- Update to 2.91.91

* Mon Feb 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-5
- Make the new if-session Autostart condition work

* Mon Feb 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-4
- Fix the autostart syntax

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-3
- Install an autostart file for the authentication agent
  in the fallback session

* Tue Feb 22 2011 Ray Strode <rstrode@redhat.com> 2.91.90-2
- Fix crashity crash crash

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- 2.91.6

* Tue Jan 25 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-3
- Just require control-center-filesystem (#661565)

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-2
- Don't run the shell on softpipe

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-7
- Rebuild against new gtk

* Sun Nov 07 2010 Ray Strode <rstrode@redhat.com> 2.91.0-6
- Fix some cases where the inhibitor dialog shows up when it isn't
  supposed to.

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-5
- Prepare for libnotify 0.7.0

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-4
- Rebuild against newer gtk3

* Tue Oct 26 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.91.0-3
- Gconf2 scriptlet accepts schema file names without file extension.

* Fri Oct 15 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.91.0-2
- Merge-review cleanup (#225835)

* Wed Oct  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Wed Sep 29 2010 jkeating - 2.31.6-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Ray Strode <rstrode@redhat.com> - 2.31.6-2
- build fixes

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Thu Jul  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Require dconf

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Fri May 07 2010 Colin Walters <walters@verbum.org> - 2.30.0-2
- Use upstream commit for library linking

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Thu Feb 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Fri Jan 15 2010 Ray Strode <rstrode@redhat.com> - 2.28.0-4
- Nag user if they try to log in as root

* Fri Nov  6 2009 Matthias Clasen  <mclasen@redhat.com> - 2.28.0-3
- Add ability to perform actions after a period of idleness

* Fri Oct 23 2009 Matthias Clasen  <mclasen@redhat.com> - 2.28.0-2
- Avoid a crash on certain xsmp error conditions

* Wed Sep 23 2009 Matthias Clasen  <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Wed Sep  9 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Thu Aug 13 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.5-2
- Require polkit-desktop-policy

* Tue Jul 28 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.4-2
- Require polkit-gnome, we need an authentication agent in the session

* Wed Jul 15 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Fri Jul 10 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-5
- Avoid pointless warnings

* Sun Jun 14 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-4
- Drop unused files

* Fri Jun 12 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-3
- Fix some oversights in the PolicyKit port

* Tue May 12 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-2
- Port to PolicyKit 1

* Tue Apr 14 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-session/2.26/gnome-session-2.26.1.news

* Wed Apr  8 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0.90-1
- Update to 2.26.0.90

* Sun Apr  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-2
- Avoid some warnings (#493688)

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Fri Mar  6 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.92-2
- Turn off excessive debug spew

* Tue Mar  3 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Thu Feb 26 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.91-4
- Make -xsession arch again
- Fix xsync usage

* Tue Feb 24 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.91-3
- Make -xsession noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Jan 20 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.5-2
- Update to 2.25.5
- Fix BuildRequires

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Thu Dec  4 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-2
- Update to 2.25.2

* Tue Nov 25 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-5
- Spec file cleanups

* Mon Nov 10 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-4
- Fix client registration in some cases 

* Sun Oct 26 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-3
- Make the capplet resizable (#468577)

* Wed Oct 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1
- Drop upstreamed patches

* Wed Oct 15 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-11
- Remove some dubious code to fix panel race at startup that
  would make shutdown menu item disappear for some users.

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-10
- Rewrite patch another time leverage better api and be more
  terse

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-9
- Bring shutdown menu item back.  More fallout from my buggy
  patch introduced in -7

* Thu Oct  9 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-8
- Fix assertion failure in last patch

* Thu Oct  9 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-7
- Add new api for panel to figure out whether or not to show
  Shutdown menu item.

* Fri Oct  3 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-6
- Fix missing translations in the capplet
- Fix small UI issues in the capplet

* Sun Sep 28 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-5
- BR xorg-x11-xtrans-devel (#464316)

* Fri Sep 26 2008 Ray Strode  <rstrode@redhat.com> - 2.24.0-4
- Make the new xsession subpackage require the version of
  gnome-session it's built against

* Thu Sep 25 2008 Ray Strode  <rstrode@redhat.com> - 2.24.0-3
- Split gnome-session.desktop off into subpackage

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0
- Drop upstreamed patches

* Thu Sep 18 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-6
- Plug memory leaks

* Thu Sep 18 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-5
- Plug memory leaks

* Mon Sep 15 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-4
- Plug memory leaks

* Sun Sep 14 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-3
- Plug memory leaks

* Sun Sep 14 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-2
- Plug memory leaks

* Mon Sep  8 2008 Jon McCann  <jmccann@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Thu Aug 28 2008 Jon McCann  <jmccann@redhat.com> - 2.23.91.0.2008.08.28.1
- Update to snapshot

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Thu Aug 14 2008 Lennart Poettering  <lpoetter@redhat.com> - 2.23.6-4
- Drop login/logout sound scripts since we do this now in libcanberra

* Tue Aug 12 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.6-3
- Fix a crash in the at-spi-registryd-wrapper

* Thu Aug  7 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.6-2
- Fix another icon name

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Wed Jul 30 2008 Jon McCann  <jmccann@redhat.com> - 2.23.6.0.2008.07.30.1
- New snapshot from DBus branch

* Mon Jul 29 2008 Jon McCann  <jmccann@redhat.com> - 2.23.6.0.2008.07.29.1
- New snapshot from DBus branch

* Mon Jul 28 2008 Jon McCann  <jmccann@redhat.com> - 2.23.5.0.2008.07.28.1
- New snapshot from DBus branch

* Thu Jul 24 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.5.0.2008.07.21.4
- Fix a crash

* Mon Jul 22 2008 Jon McCann  <jmccann@redhat.com> - 2.23.5.0.2008.07.21.3
- Add BuildRequires PolicyKit-gnome-devel

* Mon Jul 21 2008 Jon McCann  <jmccann@redhat.com> - 2.23.5.0.2008.07.21.2
- New snapshot to fix build

* Mon Jul 21 2008 Jon McCann  <jmccann@redhat.com> - 2.23.5.0.2008.07.21.1
- Snapshot from DBus branch

* Wed Jul  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4.1-4
- Fix a typo in the previous patch

* Wed Jul  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4.1-3
- Use more standard icon names

* Tue Jul  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4.1-2
- Escape comments for markup

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4.1-1
- Update to 2.23.4.1

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri May 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2.2-3
- Make nautilus start again

* Thu May 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2.2-2
- Don't crash while handling legacy sessions

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2.2-1
- Update to 2.23.2.2

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Thu Apr 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1.1-1
- Update to 2.22.1.1 (fixes a crash in the trash migration code)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Sun Apr  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Drop gnome-volume-manager from the default session

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Thu Mar 06 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.93-1
- Update to 2.21.93, drop esound dependencies and patches

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Mon Feb 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90-2
- Add patch to make login sounds work
- Remove unneeded patch to launch gnome-user-share, it launches
  using autostart now

* Tue Jan 29 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Nov 27 2007  Matthias Clasen <mclasen@redhat.com> - 2.20.2-1
- Update to 2.20.2 (translation updates)

* Tue Oct 30 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-2
- Enable sound by default, without looking at the prefs

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates)

* Thu Sep 27 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-2
- drop redhat-artwork dep.  We don't need it.

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-3
- Plug memory leaks in the ICE code

* Wed Sep  5 2007 Kristian Høgsberg <krh@redhat.com> - 2.19.92-2
- Update gnome-session-2.17.5-window-manager.patch to apply (remove
  chunks that are now upstream).

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.90-2
- Rebuild for build ID

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 2.19.6-5
- Edit window manager patch again to add 'glib' to compiz launch.

* Thu Aug  9 2007 Kristian Høgsberg <krh@redhat.com> - 2.19.6-4
- Edit the right window manager patch and delete the old one.

* Thu Aug  9 2007 Kristian Høgsberg <krh@redhat.com> - 2.19.6-3
- Export LIBGL_ALWAYS_INDIRECT before starting compiz.

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Sun Jul  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-3
- Move /usr/share/gnome/wm-properties to control-center-filesystem

* Tue Jun 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-2
- Fix a hang on login with a11y

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3
- Drop upstreamed patch

* Tue May 22 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.2-2
- Fix up logic in iris patch

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue May 15 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-7
- Don't show iris animation when using compiz (bug 237842)

* Sun May  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-6
- Don't own /usr/share/applications

* Sat Apr 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-5
- Add a dependency on dbus-x11

* Thu Apr 12 2007 David Zeuthen <davidz@redhat.com> - 2.18.0-4
- start same kind of AT's in session as started in gdm (#229912)

* Fri Mar 30 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-3
- remove xdg autostart dir since it's part of filesystem now

* Wed Mar 21 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-2
- remove eggcups from default session (bug 233261)

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Wed Feb 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Fri Feb 23 2007 Jeremy Katz <katzj@redhat.com> - 2.17.91-2
- disable a11y registry timeout so that we don't get the popup with 
  the livecd (#227214)

* Tue Feb 13 2007 Matthisa Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Tue Feb  6 2007 Kristian Høgsberg <krh@redhat.com> - 2.17.90.1-3
- Update gnome-session-2.15.90-window-manager.patch to start
  gtk-window-decorator instead of gnome-window-decorator for compiz.

  [ Update: the patch is not applied and upstream gnome-session does
    the right thing. ]

* Mon Feb  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90.1-2
- Require GConf2-gtk for gconf-sanity-check 

* Tue Jan 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90.1-1
- Update to 2.17.90.1

* Sun Jan 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90
- Clean up BuildRequires

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Mon Nov 27 2006 Ray Strode <rstrode@redhat.com> - 2.17.2-6
- don't set http_proxy variable if proxy requires password (bug
  217332)

* Wed Nov 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-4
- Own the /usr/share/gnome/wm-properties directory (#216514)

* Mon Nov 20 2006 Ray Strode <rstrode@redhat.com> - 2.17.2-3
- don't make gnome.desktop executable (bug 196105)

* Sat Nov 11 2006 Matthias Clasen  <mclasen@redhat.com> - 2.17.2-2
- Fix gnome-wm for compiz

* Tue Nov  7 2006 Matthias Clasen  <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Thu Oct 26 2006 Ray Strode <rstrode@redhat.com> - 2.16.1-2.fc7
- don't hose users with a stale http_proxy variable if they
  use autoconfiguration and uses to use manual configuration.
  Patch by Mark McLoughlin (bug 212319)

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-4
- Fix scripts according to the packaging guidelines

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-3.fc6
- Fix position of icons in the splash screen  (#205508)

* Wed Sep  6 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-2.fc6
- set http_proxy environment variable from GNOME settings 
  (bug 190041)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92
- Add %%preun and %%postun scripts

* Mon Aug 14 2006 Ray Strode <rstrode@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Sun Aug 13 2006 Ray Strode <rstrode@redhat.com> - 2.15.90-4.fc6
- fix window manager launching script. Patch from 
  Tim Vismor <tvismor@acm.org> (bug 202312)

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.15.90-3.fc6
- start gnome-window-decorator and pass "gconf" when invoking
  compiz

* Thu Aug 10 2006 Ray Strode <rstrode@redhat.com> - 2.15.90-2.fc6
- update patch from 2.15.4-3 to be more session friendly (bug 201473)

* Fri Aug  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Thu Aug  3 2006 Soren Sandmann <sandmann@redhat.com> - 2.15.4-3
- Add patch to (a) add configuration option for window manager, (b) start the window
  manager, and (c) disable splash screen by default.

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.4-2
- Add BR for dbus-glib-devel

* Thu Jul 13 2006 Ray Strode <rstrode@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.1-5.1
- rebuild

* Mon Jun 12 2006 Bill Nottingham  <notting@redhat.com> 2.15.1-5
- remove obsolete automake14 buildreq

* Fri Jun  9 2006 Matthias Clasen  <mclasen@redhat.com> 2.15.1-4
- Add more missing BuildRequires

* Tue Jun  6 2006 Matthias Clasen  <mclasen@redhat.com> 2.15.1-3
- Add BuildRequires: intltool, autoconf, automake 

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-2
- Require system-logos, not fedora-logos

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Mar 09 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-5
- fix up path creation functions 

* Thu Mar 09 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-4
- create ~/.config/autostart before trying to migrate
  session-manual to it (bug 179602).

* Mon Mar 06 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-3
- Patch from Vincent Untz to fix session editing (upstream bug 333641)
- Desensitize buttons for operations that the user isn't allowed
  to do (bug 179479).

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 2.13.92-2
- BuildRequires: gnome-desktop-devel, libX11-devel, libXt-devel

* Tue Feb 28 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-1
- Update to 2.13.92
- Add patch from CVS HEAD to maintain compatibility with
  version 2.13.91

* Thu Feb 23 2006 Ray Strode <rstrode@redhat.com> - 2.13.91-2
- take ownership of autostart dir (bug 182335)

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Jan 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.4-2
- Disable the fatal-criticals, since it crashes too much 

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Thu Jan 12 2006 Ray Strode <rstrode@redhat.com> - 2.12.0-6
- Fix screen corruption around splash screen shape (bug 177502)

* Tue Dec 20 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.0-5
- Handle shaped window for splash screen

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Alexander Larsson <alexl@redhat.com> - 2.12.0-4
- Add gnome-user-share patch

* Tue Nov 8 2005 Ray Strode <rstrode@redhat.com> - 2.12.0-3
- fix up the dummy client ids to match the id passed initially
  passed to the programs in the default session 
  (broke in last update).

* Mon Oct 31 2005 Ray Strode <rstrode@redhat.com> - 2.12.0-2
- remove rhn applet from default session
- s/magicdev/gnome-volume-manager/

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Sep  6 2005 Ray Strode <rstrode@redhat.com> - 2.11.91-3
- Don't take ownership of /usr/share/xsessions (bug 145791).

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.91-2
- rebuild for new cairo

* Tue Aug  9 2005 Ray Strode <rstrode@redhat.com> - 2.11.91-1
- Update to upstream version 2.11.91 (fixes bug 165357).
- drop some patches

* Thu Apr 18 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-2
- Install gnome.desktop to /usr/share/xsessions (bug 145791)

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-1
- Update to upstream version 2.10.0

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> 2.9.4-1
- Update to 2.9.4

* Mon Dec 20 2004 Daniel Reed <djr@redhat.com> 2.8.0-7
- rebuild for new libhowl.so.0 library (for GnomeMeeting 1.2) (this was a mistake)

* Tue Nov 02 2004 Ray Strode <rstrode@redhat.com> 2.8.0-6
- Rebuild for devel branch

 * Tue Nov 02 2004 Ray Strode <rstrode@redhat.com> 2.8.0-5
- Convert Tamil translation to UTF8 
  (Patch from Lawrence Lim <llim@redhat.com>, bug 135351)

* Fri Oct 08 2004 Ray Strode <rstrode@redhat.com> 2.8.0-4
- Add g-v-m to default session since it wasn't already (?).
- Remove g-v-m from default session on s390

* Thu Oct 07 2004 Ray Strode <rstrode@redhat.com> 2.8.0-3
- Check for NULL program name when looking for client
  match in session.

* Fri Sep 24 2004 Ray Strode <rstrode@redhat.com> 2.8.0-2
- Add "Session" item to More Preferences menu

* Fri Sep 17 2004 Ray Strode <rstrode@redhat.com> 2.8.0-1
- Update to 2.8.0 
- Remove "Session" item from Preferences menu

* Fri Sep 03 2004 Ray Strode <rstrode@redhat.com> 2.7.91-2
- Fix from Federico for infamous hanging splash screen problem.
  (http://bugzilla.gnome.org/show_bug.cgi?id=151664)

* Tue Aug 31 2004 Ray Strode <rstrode@redhat.com> 2.7.91-1
- Update to 2.7.91

* Wed Aug 18 2004 Ray Strode <rstrode@redhat.com> 2.7.4-3
- Change folder name from "autostart" to more aptly named
  "session-upgrades" from suggestion by Colin Walters.
- put non-upstream gconf key in rh_extensions

* Wed Aug 18 2004 Ray Strode <rstrode@redhat.com> 2.7.4-2
- Provide drop-a-desktop-file method of adding programs
  to the user's session.

* Fri Jul 30 2004 Ray Strode <rstrode@redhat.com> 2.7.4-1
- Update to 2.7.4

* Wed Jul 14 2004 root <markmc@localhost.localdomain> - 2.6.0-7
- Add patch to activate vino based on the "remote_access/enabled"
  preference

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Ray Strode <rstrode@redhat.com> 2.6.0-5
- Prevent having duplicate packages in different collections

* Mon Jun 14 2004 Ray Strode <rstrode@redhat.com> 2.6.0-4
- Use desktop-file-install instead of patching 
  session-properties.desktop.  Add X-Red-Hat-Base category.

* Thu Jun 10 2004 Ray Strode <rstrode@redhat.com> 2.6.0-3
- Add terminating list delimiter to OnlyShowIn entry of 
  session-properties.desktop

* Fri Apr 16 2004 Warren Togami <wtogami@redhat.com> 2.6.0-2
- #110725 BR automake14 autoconf gettext

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-1
- Update to 2.6.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com>
- Update to 2.5.91

* Tue Feb 24 2004 Mark McLoughlin <markmc@redhat.com> 2.5.90-1
- Update to 2.5.90
- Remove extraneous fontconfig BuildRequires
- Resolve conflicts with the icons and splash-repaint patches

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- Update to 2.5.3

* Wed Nov 05 2003 Than Ngo <than@redhat.com> 2.4.0-2
- don't show gnome-session-properties in KDE (bug #102533)

* Fri Aug 29 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-3
- fix up gnome.desktop location

* Fri Aug 29 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-2
- add gnome.desktop session for new gdm

* Wed Aug 27 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-1
- update to 2.3.7
- require control-center (#100562)

* Fri Aug 15 2003 Alexander Larsson <alexl@redhat.com> 2.3.6.2-1
- update for gnome 2.3

* Sun Aug 10 2003 Elliot Lee <sopwith@redhat.com> 2.2.2-4
- Rebuild

* Tue Jul 22 2003 Jonathan Blandford <jrb@redhat.com>
- at-startup patch to add let at's start

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May 27 2003 Alexander Larsson <alexl@redhat.com> 2.2.2-1
- Update to 2.2.2
- Add XRandR backport
- Fix up old patches, patch7 was upstream

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com> 2.2.0.2-5
- Wait for GSD to start before continuing with session

* Tue Feb 18 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-4
- repaint proper area of text in splash screen, #84527

* Tue Feb 18 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-3
- change icon for magicdev to one that exists in Bluecurve theme
  (part of #84491)

* Thu Feb 13 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-2
- load icons from icon theme

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-1
- 2.2.0.2

* Tue Feb  4 2003 Jonathan Blandford <jrb@redhat.com>
- remove extraneous separator.  Still ugly.

* Wed Jan 29 2003 Havoc Pennington <hp@redhat.com>
- add icons for the stuff in the default session #81489

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- 2.1.90
- drop purgedelay patch, as it was increased upstream (though only to 2 minutes instead of 5)

* Fri Dec  6 2002 Tim Waugh <twaugh@redhat.com> 2.1.2-2
- Add eggcups to default session.

* Wed Nov 13 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Tue Sep  3 2002 Owen Taylor <otaylor@redhat.com>
- Up purge delay for session manager to 5 minutes to avoid problem 
  with openoffice.org timing out

* Wed Aug 28 2002 Havoc Pennington <hp@redhat.com>
- put gdm session in here, conflict with old gdm
- use DITHER_MAX for dithering to make splash screen look good in 16
  bit

* Tue Aug 27 2002 Havoc Pennington <hp@redhat.com>
- fix missing icons and misaligned text in splash

* Fri Aug 23 2002 Tim Waugh <twaugh@redhat.com>
- Fix login sound disabling (bug #71664).

* Wed Aug 14 2002 Havoc Pennington <hp@redhat.com>
- put rhn applet in default session

* Wed Aug 14 2002 Havoc Pennington <hp@redhat.com>
- fix the session file, should speed up login a lot
- put magicdev in default session

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 2.0.5 with more translations

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.4
- remove gnome-settings-daemon from default session

* Wed Jul 31 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3
- remove splash screen, require redhat-artwork instead

* Wed Jul 24 2002 Owen Taylor <otaylor@redhat.com>
- Set GTK_RC_FILES so we can change the gtk1 theme

* Tue Jul 16 2002 Havoc Pennington <hp@redhat.com>
- pass --with-halt-command=/usr/bin/poweroff
  --with-reboot-command=/usr/bin/reboot

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.1, fixing missing po files

* Wed Jun 19 2002 Havoc Pennington <hp@redhat.com>
- put in new default session with pam-panel-icon
- disable schema install in make install, fixes rebuild failure.

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new libraries

* Thu Jun 13 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Jun 13 2002 Havoc Pennington <hp@redhat.com>
- add fix from Nalin to build require usermode

* Tue Jun 11 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- install the schemas, so we get a logout dialog and splash
- put in the splash from 7.3

* Sun Jun 09 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Sun Jun 09 2002 Havoc Pennington <hp@redhat.com>
- rebuild in new environment, require newer gtk2

* Sun Jun  9 2002 Havoc Pennington <hp@redhat.com>
- remove obsoletes/provides gnome-core

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.5.21

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.5.19
- add more build reqs to chill out build system
- provide gnome-core

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- obsolete gnome-core
- 1.5.18

* Fri Apr 19 2002 Havoc Pennington <hp@redhat.com>
- default to metacity

* Tue Apr 16 2002 Havoc Pennington <hp@redhat.com>
- Initial build.


