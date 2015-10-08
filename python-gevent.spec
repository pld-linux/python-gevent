
# TODO:
#	- test__core_stat.py fails on 32-bit builds with system libev
#	  investigate/fix that and enable system libev
#
#	- investigate some other failing tests
#	  (now excluded via known_failures-pld.patch)

# Conditional build:
%bcond_without	tests	# do not run tests
%bcond_with	system_libev	# build with system libev (more tests will fail)
%bcond_without	system_c_ares	# build with system c_ares
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define     module  gevent
Summary:	A coroutine-based Python networking library
Name:		python-%{module}
Version:	1.1b5
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/g/gevent/%{module}-%{version}.tar.gz
# Source0-md5:	e120a6672feecbbc38b2fe1757ae6099
Patch0:		known_failures-pld.patch
URL:		http://www.gevent.org/
%{?with_system_c_ares:BuildRequires:	c-ares-devel >= 1.10.0}
%{?with_system_libev:BuildRequires:	libev-devel >= 4.11}
#BuildRequires:	python-Cython
%if %{with python2}
BuildRequires:	python-devel
%if %{with tests}
BuildRequires:	python-devel-src
BuildRequires:	python-greenlet >= 0.3.2
BuildRequires:	python-test
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
%if %{with tests}
BuildRequires:	python3-greenlet >= 0.3.2
BuildRequires:	python3-test
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.688
Requires:	python-greenlet >= 0.3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gevent is a coroutine-based Python networking library.

Features include:

- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets

%package -n python3-%{module}
Summary:	A coroutine-based Python networking library
Group:		Libraries/Python
Requires:	python-greenlet >= 0.3.2

%description -n python3-%{module}
gevent is a coroutine-based Python networking library.

Features include:

- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
# when Cython-generated files are to be rebuilt
# (BR: python-Cython must be enabled then too)
# ln -s Makefile.ext Makefile

%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python} setup.py build --build-base build-2

%if %{with tests}
cd greentest
PYTHONPATH=$PWD/$(ls -1d ../build-2/lib.*) %{__python} testrunner.py --config ../known_failures.py
cd ..
%endif
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python3} setup.py build --build-base build-3

%if %{with tests}
cd greentest
PYTHONPATH=$PWD/$(ls -1d ../build-3/lib.*) %{__python3} testrunner.py --config ../known_failures.py
cd ..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_semaphore.so
%attr(755,root,root) %{py_sitedir}/%{module}/_util.so
%attr(755,root,root) %{py_sitedir}/%{module}/ares.so
%attr(755,root,root) %{py_sitedir}/%{module}/core.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py%{py_ver}.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/*.py*
%attr(755,root,root) %{py3_sitedir}/%{module}/_semaphore*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/_util*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/ares*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/core*.so
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif
