More about how our translation flow works
===========================================

.. note:: Thanks `frc-docs-translation <https://github.com/wpilibsuite/frc-docs-translations>`_ for providing us with such good resources for reference. And all of our translation works are automatic!

Introduction
---------------

There great work is done by Github Action with several automatic scripts.

How to adapt this workflow to your own project
-----------------------------------------------

1. Copy and past the `scripts/`, `.github/workflow/` and `requirements.txt` folders to your project's root directory.
2. Change the corresponding parts in `scripts/lock-translations.py`, `scripts/update.sh`, `.github/workflow/publish_main.yml`, `.github/workflow/update-translations.yml`.

In `scripts/lock-translations.py`
------------------------------------

1. Change `PROJECT_FILTER_PARAM` and `PROJECT_DELETE_PARAM`

.. tabs::

    .. code-tab:: python

        PROJECT_FILTER_PARAM = {"filter[project]": "o:Your organization on Transifex:p:Your project name"}
        PROJECT_DELETE_PARAM = {"o:Your organization on Transifex:p:Your project name:r:"}

.. note:: `Your organization on Transifex` can be found in the URL of your Transifex project. And remember that all the letters are lowercase.

1. Change content in the quotes to your project's name.

.. tabs::

    .. code-tab:: python

        section = section.split("6940swerve-docs.", 1)

In `scripts/update.sh`
------------------------------------

1. Change the `LANG_TO_PULL` and `LANG_MAP` to the language you want to be translated into.

.. code-block:: shell

        #LANG_TO_PULL=${1:-'fr_CA,es_MX,zh_CN,tr_TR,he_IL,pt'}
        LANG_TO_PULL=${1:-'zh_CN'}
        #LANG_MAP='es_MX: es, fr_CA: fr, he_IL: he, tr_TR: tr'
        LANG_MAP='zh_CN: zh_CN'

2. Change the `MAINPROJECT` name to your project's name.

.. code-block:: shell

        section = section.split("6940swerve-docs.", 1)

3. Change the last two arguments in the below to the directory to your `../source/`(where you `conf.py` locates) and the location where you want to put your `.POT` files.

.. code-block:: shell

        # Create POT Files
        sphinx-build -T -b gettext docs/source docs/pot

4. Change the two **docs/pot** and **docs/locales** in the below image to the directory where your `.POT` files locate and where your translation files(which can also be called `.PO` files) locate.

.. code-block:: shell

        sphinx-intl update-txconfig-resources -p docs/pot -d docs/locales --transifex-project-name $MAINPROJECT

In `.github/workflow/publish_main.yml`
-----------------------------------------

You know which parts should be changed and l won't go into it here.

In `.github/workflow/update-translations.yml`
-------------------------------------------------

1. Change the `github.repository` to your own repo.
2. If you don't have a Submodule, just annotate the related three lines.
3. Create a repository secret in your repository's settings , name it as `TX_TOKEN` and paste your Transifex api token in the secret.

**Now you can test whether your workflow works well!**