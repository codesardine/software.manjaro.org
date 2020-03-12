#!/usr/bin/env python3
import discover.pamac as pamac
import cProfile
p = cProfile.Profile()
p.enable()
packages = pamac.Get.all_repo_pkgs("Packages")

for pkg in packages:
    pkg.get_name()

p.disable()
p.print_stats()
