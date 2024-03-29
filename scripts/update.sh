#!/bin/sh
# update transifex pot and local po files

set -ex

#LANG_TO_PULL=${1:-'fr_CA,es_MX,zh_CN,tr_TR,he_IL,pt'}
LANG_TO_PULL=${1:-'zh_CN'}
#LANG_MAP='es_MX: es, fr_CA: fr, he_IL: he, tr_TR: tr'
LANG_MAP='zh_CN: zh_CN'
MAINPROJECT=6940swerve-docs
ORGANIZATION=frc-team-6940-1

# Set working directory to repo root
cd `dirname $0`/..

# Create POT Files
sphinx-build -T -b gettext docs/source docs/pot

# Update .tx/config
rm .tx/config
sphinx-intl create-txconfig
echo "lang_map = ${LANG_MAP}" >> .tx/config
# sphinx-intl update-txconfig-resources -p docs/pot -d docs/locales --transifex-project-name $MAINPROJECT
sphinx-intl update-txconfig-resources -p docs/pot -d docs/locales --transifex-project-name $MAINPROJECT --transifex-organization-name $ORGANIZATION


# Push and pull from Transifex. It is important to push then pull!
# If you pull then push, the PO files will contain out of date strings.
if [ "$CI" = true ]
then
    # tx push --source --no-interactive --skip
    tx push --source --skip
fi
tx pull -l $LANG_TO_PULL --mode onlyreviewed --use-git-timestamps
