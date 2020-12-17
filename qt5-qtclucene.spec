%define		qtbase_ver	%{version}
Summary:	Legacy Qt5 CLucene library
Summary(pl.UTF-8):	Stara biblioteka Qt5 CLucene
Name:		qt5-qtclucene
Version:	5.8.0
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/new_archive/qt/5.8/%{version}/submodules/qttools-opensource-src-%{version}.tar.xz
# Source0-md5:	506e53a228fe0c3d6c8b6fbebd8e47ae
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains the legacy CLucene library, dropped in Qt 5.9.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera starą bibliotekę CLucene, porzuconą w Qt 5.9.

%package -n Qt5CLucene
Summary:	Qt5 CLucene library
Summary(pl.UTF-8):	Biblioteka Qt5 CLucene
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}

%description -n Qt5CLucene
The Qt5 CLucene library provides Qt API to CLucene, a C++ port of
Lucene high-performance, full-featured text search engine.

%description -n Qt5CLucene -l pl.UTF-8
Biblioteka Qt5 CLucene dostarcza API Qt do CLucene - portu C++
wysoko wydajnego, w pełni funkcjonalnego silnika wyszukiwania
pełnotekstowego.

%package -n Qt5CLucene-devel
Summary:	Qt5 CLucene library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 CLucene - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5CLucene = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Obsoletes:	qt5-qttools-devel < 5.2.0-1

%description -n Qt5CLucene-devel
Header files for Qt5 CLucene library.

%description -n Qt5CLucene-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 CLucene.

%prep
%setup -q -n qttools-opensource-src-%{version}

%build
cd src/assistant/clucene
qmake-qt5
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src/assistant/clucene install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# kill unnecessary -L%{_libdir} from *.la, *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.{la,prl}

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*Qt5*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5CLucene -p /sbin/ldconfig
%postun	-n Qt5CLucene -p /sbin/ldconfig

%files -n Qt5CLucene
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5CLucene.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5CLucene.so.5

%files -n Qt5CLucene-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5CLucene.so
%{_libdir}/libQt5CLucene.prl
%{_includedir}/qt5/QtCLucene
%{qt5dir}/mkspecs/modules/qt_lib_clucene_private.pri
%{_libdir}/cmake/Qt5CLucene
