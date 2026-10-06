# Noctis profile

Original vector artwork for the JEMostert GitHub profile. The visual system uses a midnight sky, violet and blue crystals, orbital geometry, and a royal blade. It is inspired by Noctis without copying game artwork or logos.

## Update

```sh
python3 scripts/build_art.py
python3 scripts/update_observatory.py
```

`build_art.py` creates the hero, project cards, LabServant panel, footer, and local badges. SVGs contain no JavaScript, external fonts, or embedded remote resources. Motion is decorative; reduced-motion preferences disable it. Compact variants are selected through GitHub-supported picture elements. Markdown contains the project descriptions so the content stays readable and selectable.

`update_observatory.py` reads public GitHub endpoints only. It excludes forks and the profile repository from original-build statistics, and counts distinct primary languages rather than claiming language proficiency or measuring private work. It writes desktop and compact SVGs from the same response. API failures preserve the last successful artwork.

The daily GitHub Actions workflow commits only changed observatory files. It uses the repository's temporary GitHub token and requires no personal token or third-party stats service. Official actions are pinned to commit hashes.

Project screenshots are served from their public source repositories and are labeled with their source context. The LabServant section describes broad work areas; it contains no private source, customer information, internal issue links, or unreleased feature claims.
