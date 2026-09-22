%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: nginx_exporter
Version: 1.5.3
Release: 1%{?dist}
Summary: NGINX Prometheus Exporter for NGINX and NGINX Plus.
License: ASL 2.0
URL:     https://github.com/nginxinc/nginx-prometheus-exporter

Source0: https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v%{version}/nginx-prometheus-exporter_%{version}_linux_amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
NGINX Prometheus Exporter for NGINX and NGINX Plus.

%prep
%setup -q -D -c nginx-prometheus-exporter_%{version}_linux_amd64
mv -v nginx-prometheus-exporter %{name}

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Tue Sep 22 2026 Ivan Garcia
- Bump version to 1.5.3
* Thu Apr 15 2026 Ivan Garcia <igarcia@cloudox.org> - 1.5.1
- Initial packaging for the 1.5.1 branch
