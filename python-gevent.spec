
# TODO:
#	- investigate some of the failing tests
#	  (now excluded via known_failures-pld.txt)

# Conditional build:
%bcond_without	tests	# do not run tests

%define     module  gevent
Summary:	A coroutine-based Python networking library
Name:		python-%{module}
Version:	1.0
Release:	1
License:	MIT
Group:		Development/Languages
URL:		http://www.gevent.org/
Source0:	http://pypi.python.org/packages/source/g/gevent/%{module}-%{version}.tar.gz
# Source0-md5:	33aef51a06268f5903fea378e1388e4d
Source1:	known_failures-pld.txt
BuildRequires:	libevent-devel >= 1.4.0
BuildRequires:	python-devel
%{?with_tests:BuildRequires: python-test}
BuildRequires:	rpm-pythonprov
Requires:	python-greenlet
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gevent is a coroutine-based Python networking library that uses
greenlet to provide a high-level synchronous API on top of libevent
event loop.

Features include:
  - convenient API around greenlets
  - familiar synchronization primitives (gevent.event, gevent.queue)
  - socket module that cooperates
  - WSGI server on top of libevent-http
  - DNS requests done through libevent-dns
  - monkey patching utility to get pure Python modules to cooperate

%prep
%setup -q -n %{module}-%{version}

cat known_failures.txt %{SOURCE1} > known_failures-merged.txt

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
    --skip-build \
    --optimize=2 \
    --root=$RPM_BUILD_ROOT

%py_postclean

%if %{with tests}
cd greentest
PYTHONPATH=.. python testrunner.py --expected ../known_failures-merged.txt
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/core.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py%{py_ver}.egg-info
%endif
