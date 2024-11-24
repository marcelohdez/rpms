%bcond_without check

%global crate dim-screen

Name:           dim-screen
Version:        0.3.0
Release:        %autorelease
Summary:        Native Wayland screen dimming tool

SourceLicense:  GPL-3.0-only
License:        GPL-3.0-only
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/marcelohdez/dim
Source:         %{url}/archive/v%{version}/dim-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 26, scdoc, gzip

%global _description %{expand:
Native Wayland screen dimming tool.}

%description %{_description}

%prep
%autosetup -p1 -n dim-%{version}
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

# generate shell completions to be installed later
target/release/dim --gen-completions .

# build manpages and gzip them in the target dir:
scdoc < man/dim.1.scd > man/dim.1
gzip man/dim.1

%install
install -Dpm755 target/release/dim  %{buildroot}%{_bindir}/dim
install -Dpm644 _dim                %{buildroot}%{zsh_completions_dir}/_dim
install -Dpm644 dim.bash            %{buildroot}%{bash_completions_dir}/dim
install -Dpm644 dim.fish            %{buildroot}%{fish_completions_dir}/dim.fish
install -Dpm644 man/dim.1.gz -t     %{buildroot}%{_mandir}/man1

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/dim
%{_mandir}/man1/dim.1*
%{bash_completions_dir}/dim
%{fish_completions_dir}/dim.fish
%{zsh_completions_dir}/_dim

%changelog
%autochangelog
