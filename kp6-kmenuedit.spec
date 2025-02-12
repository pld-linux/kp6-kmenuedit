#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.0
%define		qtver		5.15.2
%define		kpname		kmenuedit

Summary:	KDE menu editor
Name:		kp6-%{kpname}
Version:	6.3.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	a6bb60b5d9d4ce40243d104219d4b5de
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kf6-sonnet-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Plasma menu editor.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kmenuedit
%{_desktopdir}/org.kde.kmenuedit.desktop
%{_iconsdir}/hicolor/*/apps/kmenuedit.png
%{_datadir}/kmenuedit
%{_datadir}/qlogging-categories6/kmenuedit.categories
%{_datadir}/metainfo/org.kde.kmenuedit.appdata.xml
