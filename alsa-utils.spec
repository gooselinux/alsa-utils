#define  prever         rc3
#define  prever_dot     .rc3

Summary: Advanced Linux Sound Architecture (ALSA) utilities
Name:    alsa-utils
Version: 1.0.21
Release: 3%{?prever_dot}%{?dist}
License: GPLv2+
Group:   Applications/Multimedia
URL:     http://www.alsa-project.org/
Source:  ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}%{?prever}.tar.bz2
Source4: alsaunmute
Source6: alsa-info.sh
Source10: alsa.rules
Source11: alsactl.conf
Patch1:  alsactl-init-fix-headphone2.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: alsa-lib-devel >= %{version}
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: xmlto
Conflicts: udev < 062

%description
This package contains command line utilities for the Advanced Linux Sound
Architecture (ALSA).

%prep
%setup -q -n %{name}-%{version}%{?prever}
%patch1 -p1 -b .headphone

%build
%configure CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" --sbindir=/sbin --disable-alsaconf
%{__make} %{?_smp_mflags}
%{__cp} %{SOURCE4} .

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

# Install ALSA udev rules
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/udev/rules.d
install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/udev/rules.d/90-alsa.rules

# Install support utilities
mkdir -p -m755 $RPM_BUILD_ROOT/bin
install -p -m 755 alsaunmute %{buildroot}/bin/

# Link alsactl to /usr/sbin
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
ln -s ../../sbin/alsactl $RPM_BUILD_ROOT/%{_sbindir}/alsactl

# Move /usr/share/alsa/init to /lib/alsa/init
mkdir -p -m 755 %{buildroot}/lib/alsa
mv %{buildroot}%{_datadir}/alsa/init %{buildroot}/lib/alsa

# Link /lib/alsa/init to /usr/share/alsa/init back
ln -s ../../../lib/alsa/init %{buildroot}%{_datadir}/alsa/init

# Create a place for global configuration
mkdir -p -m 755 %{buildroot}/etc/alsa
install -p -m 644 %{SOURCE11} %{buildroot}/etc/alsa
touch %{buildroot}/etc/asound.state

# Install alsa-info.sh script
install -p -m 755 %{SOURCE6} %{buildroot}/usr/bin/alsa-info
ln -s alsa-info %{buildroot}/usr/bin/alsa-info.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%config /etc/udev/rules.d/*
%config /etc/alsa/*
/bin/*
/sbin/*
/lib/alsa/init/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/alsa/
%{_datadir}/sounds/
%{_mandir}/man?/*
%dir /etc/alsa/
%dir /lib/alsa/
%dir /lib/alsa/init/
%ghost /etc/asound.state

%post
if [ -s /etc/alsa/asound.state -a ! -s /etc/asound.state ] ; then
  mv /etc/alsa/asound.state /etc/asound.state
fi

%changelog
* Tue Apr 20 2010 Jaroslav Kysela <jkysela@redhat.com> 1.0.21-3
- fix macro references in changelog

* Thu Sep  3 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.21-2
- added missing patch file

* Thu Sep  3 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.21-1
- updated to 1.0.21 final
- updated alsa-info.sh script to 0.4.58

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.20-3
- added missing Headphone Volume patch

* Fri May 15 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.20-2
- fixed Headphone Volume issue (bz#500956)

* Wed May 06 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.20-1
- updated to 1.0.20 final
- updated alsa-info.sh script to 0.4.56

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.19-3
- fixed volume initialization for some HDA codecs
- updated alsa-info.sh to 0.4.54

* Wed Feb 04 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.19-2
- add %%dir directive for /lib/alsa and /lib/alsa/init directories (bz#483324)

* Tue Jan 20 2009 Jaroslav Kysela <jkysela@redhat.com> 1.0.19-1
- updated to 1.0.19 final

* Tue Nov 04 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.18-5
- fixed building

* Tue Nov 04 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.18-4
- updated to 1.0.18 final
- updated alsa-info.sh script

* Thu Sep 18 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.18-3.rc3
- fixed alsa-info.sh link

* Thu Sep 18 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.18-2.rc3
- fixed /lib/alsa/init path for x86_64 (was /lib64/alsa/init)
- added /etc/alsa/asound.state -> /etc/asound.state shift to %%post section
- fix udev rules (ommited /dev/ prefix for the alsactl utility)
- added --ignore option for alsactl (added also to upstream)

* Thu Sep 11 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.18-1.rc3
- updated to 1.0.18rc3
- updated alsa-info.sh script to 0.4.51
- removed alsacard utility
- removed salsa utility
- changed alsaunmute to use 'alsactl init' now
- updated ALSA udevd rules to use alsactl
- moved /etc/alsa/asound.state back to /etc/asound.state

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> 1.0.17-1
- updated to 1.0.17 final
- updated alsa-info.sh script to 0.4.48

* Mon Apr 28 2008 Martin Stransky <stransky@redhat.com> 1.0.16-3
- Added alsa-info.sh script to /usr/bin/alsa-info

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.16-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Martin Stransky <stransky@redhat.com> 1.0.16-1
- updated to 1.0.16 final

* Tue Jan 15 2008 Mikel Ward <mikel@mikelward.com>
- add salsa man page

* Mon Oct 29 2007 Martin Stransky <stransky@redhat.com> 1.0.15-1
- updated to 1.0.15 final

* Mon Oct 1 2007 Martin Stransky <stransky@redhat.com> 1.0.15-0.4.rc1
- moved saved volume settings back to /etc/alsa
  (per discussion at #293301)

* Mon Sep 24 2007 Martin Stransky <stransky@redhat.com> 1.0.15-0.3.rc1
- fixed #303151 - wrong salsa dir in /etc/udev/rules.d/90-alsa.rules

* Thu Sep 20 2007 Matthias Saou <http://freshrpms.net/> 1.0.15-0.2.rc1
- Update License field.
- Mark udev rule as config.
- Use find_lang macro again to include translations (why was it removed?).

* Wed Sep 19 2007 Martin Stransky <stransky@redhat.com> 1.0.15-0.1.rc1
- new upstream
- moved saved volume settings to /var/lib (#293301)
- patched alsactl for that (#255421)

* Thu Aug 16 2007 Martin Stransky <stransky@redhat.com> 1.0.14-2
- added an entry to alsaunmute for HP xw4550 (#252171)

* Wed Jul 25 2007 Martin Stransky <stransky@redhat.com> 1.0.14-1
- release bump

* Thu Jun 7 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.8
- new upstream

* Wed May 30 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.7.rc2
- updated alsanumute for Siemens Lifebook S7020 (#241639)
- unmute Master Mono for all drivers

* Wed May 2 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.6.rc2
- added fix for #238442 (unmute Mono channel for w4550, 
  xw4600, xw6600, and xw8600)

* Wed Apr 18 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.5.rc2
- added more funcionality to salsa (save/load sound settings),
  moved volume settings to /etc/alsa/

* Thu Apr 10 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.4.rc2
- added support for large files
- minor fix in alsaunmute
- fixed #209239 - alsaconf: Stale language-dependent files
- fixed #233765 - alsa-utils : unowned directories

* Fri Jan 19 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.3.rc2
- new upstream

* Wed Jan 10 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.2.rc1
- added a config line for hda-intel driver

* Mon Dec 11 2006 Martin Stransky <stransky@redhat.com> 1.0.14-0.1.rc1
- new upstream

* Mon Oct 2 2006 Martin Stransky <stransky@redhat.com> 1.0.12-3
- fix for #207384 - Audio test fails during firstboot

* Fri Aug 25 2006 Martin Stransky <stransky@redhat.com> 1.0.12-2
- new upstream

* Mon Aug 07 2006 Martin Stransky <stransky@redhat.com> 1.0.12-1.rc2
- new upstream

* Thu Jul 20 2006 Martin Stransky <stransky@redhat.com> 1.0.12-1.rc1
- new upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue May 30 2006 Martin Stransky <stransky@redhat.com> 1.0.11-7
- new upstream

* Wed May 3  2006 Martin Stransky <stransky@redhat.com> 1.0.11-6.rc2
- removed HW specific switch - it should be set by driver

* Thu Apr 6  2006 Martin Stransky <stransky@redhat.com> 1.0.11-5.rc2
- fixed rules file (#186494)
- fixed Audigi mixer switch (#187807)

* Mon Feb 20 2006 Martin Stransky <stransky@redhat.com> 1.0.11-3.rc2
- removed autoreconf

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-2.rc2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-2.rc2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Martin Stransky <stransky@redhat.com> 1.0.11-2.rc2
- added volume option to alsaunmute utility (for s-c-s)

* Thu Jan 12 2006 Martin Stransky <stransky@redhat.com> 1.0.11-1.rc2
- new upstream

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 24 2005 Martin Stransky <stransky@redhat.com> 1.0.10rf-1
- new upstream version
- added alias for snd-azx

* Wed Nov 9 2005 Martin Stransky <stransky@redhat.com> 1.0.10rc1-2
- fix for #169292 - RHEL4U2 xw4300 IntelHD internal speakers muted by default

* Tue Sep 27 2005 Martin Stransky <stransky@redhat.com> 1.0.10rc1-1
- new upstream version

* Tue Aug 23 2005 Martin Stransky <stransky@redhat.com> 1.0.9-5
- unmute External Amplifier by default (#166153)

* Wed Jul 13 2005 Bill Nottingham <notting@redhat.com> 1.0.9-4
- migrate the alsa restore program to a udev rule, not a dev.d program
- conflict with appropriate udev
- move alsaunmute, alsacard to /bin

* Mon Jul 11 2005 Martin Stransky <stransky@redhat.com> 1.0.9-3
- New alsaunmute utility
- Add autoconf to BuildRequires (#162483)

* Thu Jun 16 2005 Martin Stransky <stransky@redhat.com> 1.0.9-2
- New upstream version

* Mon May 30 2005 Martin Stransky <stransky@redhat.com> 1.0.9-1
- New upstream version.
- moved alsacard utility from alsa-lib to alsa-tools

* Mon May 16 2005 Bill Nottingham <notting@redhat.com> 1.0.9rc2-2
- make sure 'Wave' playback channel isn't muted (#157850)

* Mon Apr 25 2005 Martin Stransky <stransky@redhat.com> 1.0.9rc2-1
- New upstream version
- add %%find_lang macro (#155719)

* Fri Apr 1 2005 Bill Nottingham <notting@redhat.com> 1.0.8-4
- replace the dev.d script with a program that calls alsactl to
  restore the volume if there is a saved config, and just unmutes
  the playback channels if there isn't one (#132575)

* Mon Mar 7 2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Wed Feb 16 2005 Martin Stransky <stransky@redhat.com> 1.0.8-2
- fix #148011 (add gettext-devel to BuildRequires)
- add $RPM_OPT_FLAGS to CFLAGS

* Wed Jan 26 2005 Martin Stransky <stransky@redhat.com> 1.0.8-1
- update to 1.0.8
- temporarily removed alsa-lauch.patch

* Sat Jan 08 2005 Colin Walters <walters@redhat.com> 1.0.7-2
- New patch alsa-utils-1.0.7-alsa-launch.patch, adds the
  alsa-launch command.
- New source file xinit-alsa-launch.sh, integrates alsa-launch
  into X startup
- BR xorg-x11-devel

* Thu Jan 06 2005 Colin Walters <walters@redhat.com> 1.0.7-1
- New upstream version

* Tue Oct 19 2004 Bill Nottingham <notting@redhat.com> 1.0.6-3
- tweak dev.d sound restore script (#133535, revisited)

* Thu Oct 14 2004 Bill Nottingham <notting@redhat.com> 1.0.6-2
- move alsactl to /sbin
- include a dev.d script for mixer restoring (#133535)

* Mon Aug 30 2004 Bill Nottingham <notting@redhat.com> 1.0.6-1
- update to 1.0.6

* Fri Jul  2 2004 Bill Nottingham <notting@redhat.com> 1.0.5-1
- update to 1.0.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1.0.3-1
- update to 1.0.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2

* Wed Dec 17 2003 Bill Nottingham <notting@redhat.com> 1.0.0-0.rc2
- import fedora.us RPM, take out save-alsamixer & alsaconf for now

* Thu Dec 11 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.4.rc2
- rename alsamixer-saver save-alsamixer

* Mon Dec  8 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.3.rc2
- Integrate Michael Schwendt's script alsamixer-saver; Still not quite sure if 
  this script is the right way -- but mine didn't work...

* Sat Dec  6 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.2.rc2
- Update to 1.0.0rc2 
- added alsamixer Script -- stores settings on shutdown, does nothing on startup
- some minor corrections in spec-file style

* Wed Dec  3 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.1.rc1
- Update to 1.0.0rc1 

* Wed Aug  6 2003 Dams <anvil[AT]livna.org> 0:utils-0.fdr.1
- Initial build.
