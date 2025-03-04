from typing import List, Set, Optional, Iterable, Tuple

from bauh.api.abstract.model import SoftwarePackage, CustomSoftwareAction
from bauh.commons import resource
from bauh.gems.arch import ROOT_DIR, ARCH_CACHE_DIR
from bauh.view.util.translation import I18n


class ArchPackage(SoftwarePackage):

    __action_allow_rebuild_check: Optional[CustomSoftwareAction] = None
    __action_enable_pkgbuild_edition: Optional[CustomSoftwareAction] = None
    __action_disable_pkgbuild_edition: Optional[CustomSoftwareAction] = None
    __action_reinstall: Optional[CustomSoftwareAction] = None
    __action_ignore_rebuild_check: Optional[CustomSoftwareAction] = None
    __cached_attrs: Optional[Tuple[str, ...]] = None
    __dynamic_categories: Optional[Tuple[str, ...]] = None

    @classmethod
    def action_allow_rebuild_check(cls) -> CustomSoftwareAction:
        if not cls.__action_allow_rebuild_check:
            cls.__action_allow_rebuild_check = CustomSoftwareAction(i18n_label_key='arch.action.rebuild_check.allow',
                                                                    i18n_status_key='arch.action.rebuild_check.allow.status',
                                                                    i18n_confirm_key='arch.action.rebuild_check.allow.confirm',
                                                                    i18n_description_key='arch.action.rebuild_check.allow.desc',
                                                                    requires_root=False,
                                                                    manager_method='set_rebuild_check',
                                                                    icon_path=resource.get_path('img/check.svg', ROOT_DIR))

        return cls.__action_allow_rebuild_check

    @classmethod
    def action_enable_pkgbuild_edition(cls) -> CustomSoftwareAction:
        if not cls.__action_enable_pkgbuild_edition:
            cls.__action_enable_pkgbuild_edition = CustomSoftwareAction(i18n_label_key='arch.action.enable_pkgbuild_edition',
                                                                        i18n_status_key='arch.action.enable_pkgbuild_edition.status',
                                                                        i18n_confirm_key='arch.action.enable_pkgbuild_edition.confirm',
                                                                        i18n_description_key='arch.action.enable_pkgbuild_edition.desc',
                                                                        requires_root=False,
                                                                        manager_method='enable_pkgbuild_edition',
                                                                        icon_path=resource.get_path('img/mark_pkgbuild.svg', ROOT_DIR))

        return cls.__action_enable_pkgbuild_edition

    @classmethod
    def action_disable_pkgbuild_edition(cls) -> CustomSoftwareAction:
        if not cls.__action_disable_pkgbuild_edition:
            cls.__action_disable_pkgbuild_edition = CustomSoftwareAction(i18n_label_key='arch.action.disable_pkgbuild_edition',
                                                                         i18n_status_key='arch.action.disable_pkgbuild_edition',
                                                                         i18n_confirm_key='arch.action.disable_pkgbuild_edition.confirm',
                                                                         i18n_description_key='arch.action.disable_pkgbuild_edition.desc',
                                                                         requires_root=False,
                                                                         manager_method='disable_pkgbuild_edition',
                                                                         icon_path=resource.get_path('img/unmark_pkgbuild.svg', ROOT_DIR))

        return cls.__action_disable_pkgbuild_edition

    @classmethod
    def action_reinstall(cls) -> CustomSoftwareAction:
        if not cls.__action_reinstall:
            cls.__action_reinstall = CustomSoftwareAction(i18n_label_key='arch.action.reinstall',
                                                          i18n_status_key='arch.action.reinstall.status',
                                                          i18n_confirm_key='arch.action.reinstall.confirm',
                                                          i18n_description_key='arch.action.reinstall.desc',
                                                          requires_root=True,
                                                          manager_method='reinstall',
                                                          icon_path=resource.get_path('img/build.svg', ROOT_DIR))

        return cls.__action_reinstall

    @classmethod
    def action_ignore_rebuild_check(cls) -> CustomSoftwareAction:
        if not cls.__action_ignore_rebuild_check:
            cls.__action_ignore_rebuild_check = CustomSoftwareAction(i18n_label_key='arch.action.rebuild_check.ignore',
                                                                     i18n_status_key='arch.action.rebuild_check.ignore.status',
                                                                     i18n_confirm_key='arch.action.rebuild_check.ignore.confirm',
                                                                     i18n_description_key='arch.action.rebuild_check.ignore.desc',
                                                                     requires_root=False,
                                                                     manager_method='set_rebuild_check',
                                                                     icon_path=resource.get_path('img/check_disabled.svg', ROOT_DIR))

        return cls.__action_ignore_rebuild_check

    @classmethod
    def cached_attrs(cls) -> Tuple[str, ...]:
        if cls.__cached_attrs is None:
            cls.__cached_attrs = ('command', 'icon_path', 'repository', 'maintainer', 'desktop_entry', 'categories',
                                  'last_modified', 'commit')

        return cls.__cached_attrs

    @classmethod
    def dynamic_categories(cls) -> Tuple[str, ...]:
        if cls.__dynamic_categories is None:
            cls.__dynamic_categories = ('orphan', 'out_of_date')

        return cls.__dynamic_categories

    def __init__(self, name: str = None, version: str = None, latest_version: str = None, description: str = None,
                 package_base: str = None, votes: int = None, popularity: float = None,
                 first_submitted: Optional[int] = None, last_modified: Optional[int] = None,
                 maintainer: str = None, url_download: str = None, pkgbuild: str = None, repository: str = None,
                 desktop_entry: str = None, installed: bool = False, srcinfo: dict = None, dependencies: Set[str] = None,
                 categories: List[str] = None, i18n: I18n = None, update_ignored: bool = False, arch: str = None,
                 pkgbuild_editable: bool = None, install_date: Optional[int] = None, commit: Optional[str] = None,
                 require_rebuild: bool = False, allow_rebuild: Optional[bool] = None, aur_update: bool = False,
                 out_of_date: Optional[bool] = None):

        super(ArchPackage, self).__init__(name=name, version=version, latest_version=latest_version, description=description,
                                          installed=installed, categories=categories)
        self.package_base = package_base
        self.votes = votes
        self.popularity = popularity
        self.maintainer = maintainer if maintainer else (repository if repository != 'aur' else None)
        self.url_download = url_download
        self.first_submitted = first_submitted
        self.last_modified = last_modified
        self.pkgbuild = pkgbuild
        self.repository = repository
        self.command = None
        self.icon_path = None
        self.desktop_entry = desktop_entry
        self.src_info = srcinfo
        self.dependencies = dependencies
        self.arch = arch
        self.i18n = i18n
        self.update_ignored = update_ignored
        self.view_name = name  # name displayed on the view
        self.pkgbuild_editable = pkgbuild_editable  # if the PKGBUILD can be edited by the user (only for AUR)
        self.install_date = install_date
        self.commit = commit  # only for AUR for downgrading purposes
        self.require_rebuild = require_rebuild
        self.allow_rebuild = allow_rebuild
        self.aur_update = aur_update
        self.out_of_date = out_of_date

    @staticmethod
    def disk_cache_path(pkgname: str):
        return f'{ARCH_CACHE_DIR}/installed/{pkgname}'

    def get_pkg_build_url(self):
        if self.package_base:
            return 'https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=' + self.package_base

    def has_history(self):
        return self.can_be_downgraded()

    def has_info(self):
        return True

    def can_be_installed(self) -> bool:
        if super(ArchPackage, self).can_be_installed():
            return bool(self.url_download) if self.repository == 'aur' else True

    def can_be_downgraded(self):
        return self.installed and self.repository == 'aur'

    def get_type(self):
        return 'aur' if self.repository == 'aur' else 'arch_repo'

    def get_default_icon_path(self) -> str:
        return self.get_type_icon_path()

    def get_disk_icon_path(self) -> str:
        return self.icon_path

    def get_type_icon_path(self):
        return resource.get_path('img/{}.svg'.format('arch' if self.get_type() == 'aur' else 'repo'), ROOT_DIR)

    def is_application(self):
        return self.can_be_run()

    def get_base_name(self) -> str:
        return self.package_base if self.package_base else self.name

    def supports_disk_cache(self):
        return True

    def get_disk_cache_path(self) -> str:
        if self.name:
            return self.disk_cache_path(self.name)

    def get_data_to_cache(self) -> dict:
        cache = {}

        # required attrs to cache
        for a in self.cached_attrs():
            val = getattr(self, a)

            if val:
                if a == 'categories' and isinstance(val, list):
                    for cat in self.dynamic_categories():
                        if cat in val:
                            val.remove(cat)

                cache[a] = val

        return cache

    def fill_cached_data(self, data: dict):
        if data:
            for a in self.cached_attrs():
                val = data.get(a)
                if val:
                    setattr(self, a, val)

                    if a == 'icon_path':
                        self.icon_url = val

    def can_be_run(self) -> bool:
        # only returns if there is a desktop entry set for the application to avoid running command-line applications
        return bool(self.desktop_entry) and bool(self.command)

    def get_publisher(self):
        return self.maintainer

    def set_icon(self, paths: List[str]):
        self.icon_path = paths[0]

        if len(paths) > 1:
            for path in paths:
                if '/' in path:
                    self.icon_path = path
                    break

        self.icon_url = self.icon_path

    def has_screenshots(self) -> bool:
        return False

    def get_name_tooltip(self) -> str:
        return '{} ( {}: {} )'.format(self.name, self.i18n['repository'], self.repository)

    def supports_backup(self) -> bool:
        return True

    def is_update_ignored(self) -> bool:
        return self.update_ignored

    def supports_ignored_updates(self) -> bool:
        return self.installed

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} (name={}, command={}, icon_path={})'.format(self.__class__.__name__, self.name, self.command, self.icon_path)

    def __eq__(self, other):
        if isinstance(other, ArchPackage):
            if self.view_name is not None and other.view_name is not None:
                return self.view_name == other.view_name and self.repository == other.repository
            
            return self.name == other.name and self.repository == other.repository

    def get_cached_pkgbuild_path(self) -> str:
        return '{}/PKGBUILD'.format(self.get_disk_cache_path())

    def get_custom_actions(self) -> Optional[Iterable[CustomSoftwareAction]]:
        if self.installed and self.repository == 'aur':
            actions = [self.action_reinstall()]

            if self.pkgbuild_editable is not None:
                actions.append(self.action_disable_pkgbuild_edition() if self.pkgbuild_editable else self.action_enable_pkgbuild_edition())

            if self.allow_rebuild is not None:
                actions.append(self.action_ignore_rebuild_check() if self.allow_rebuild else self.action_allow_rebuild_check())

            return actions

    def get_update_tip(self) -> Optional[str]:
        if self.repository == 'aur' and self.allow_rebuild and self.require_rebuild:
            return self.i18n['arch.package.requires_rebuild'] + ' (rebuild)'

    def update_state(self):
        if self.repository == 'aur':
            if self.allow_rebuild and self.require_rebuild:
                self.update = True
            else:
                self.update = self.aur_update

    def __hash__(self):
        if self.view_name is not None:
            return hash((self.view_name, self.repository))
        else:
            return hash((self.name, self.repository))

    @property
    def orphan(self) -> bool:
        return self.maintainer is None
