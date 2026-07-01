# scaling-waffle
A documentation enhancement tool that turns raw bullet points into organized Markdown files

## Kickstart from a local zip file

Use the bootstrap script to populate this repository from a zip archive that already
exists on your machine:

```bash
python3 ./scripts/kickstart_from_zip.py /path/to/source.zip \
  --destination "$(pwd)" \
  --strip-components 1
```

Notes:

- `--destination` defaults to the current working directory.
- `--strip-components` is useful when the zip contains a single top-level folder.
- Existing files are protected by default; pass `--force` if you want to overwrite them.
- `.git` content inside the archive is ignored.
