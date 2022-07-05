Translation
===============

6940swerve-docs supports translations using the web based `Transifex <https://www.transifex.com/>`_
utility. 6940swerve-docs has been partly translated into Chinese - China (zh_CN). Translators who are
are fluent in both English and one of the specified languages would be greatly appreciated to contirbute
to the translations. Even once a translation is complete, it needs to be updated to keep up with changes
in 6940swerve-docs.

Workflow
------------

Here are some steps to follow for translating 6940swerve-docs.

1. Sign up for `Transifex <https://www.transifex.com/>`_ and ask to join the `6940swerve-docs <https://www.transifex.com/frc-team-6940-1/6940swerve-docs>`_ project, and request access to the language you'd like to contribute to.
2. Join GitHub `discussions <https://github.com/mendax1234/6940Swerve-docs/discussions>`_! This is a direct means of communication with me. You can use this to ask me questions in a fast and streamlined fashion.
3. You may be contacted and asked questions involving contributing languages before being granted access to the 6940swerve-docs translation project.
4. Translate your language!

.. important:: Since we have enabled **Tansifex Memory** function in our project, you had better check whether there is a suggestion for your translation at the bottom right (due to our automatic lock-file mechanism, the file you are translating now may have already been translated by other people). 


Links
------

Links must be preserved in their original syntax. To translate a link, you can replace the TRANSLATE ME text (this will be replaced with the English title) with the appropriate translation.

An example of the original text may be

.. code-block:: text

   For complete wiring instructions/diagrams, please see the :doc:`Wiring the FRC Control System Document <Wiring the FRC Control System document>`.

where the ``Wiring the FRC Control System Document`` then gets translated.

.. code-block:: text

   For complete wiring instructions/diagrams, please see the :doc:`TRANSLATED TEXT <Wiring the FRC Control System document>`.

Another example is below

.. code-block:: text

  For complete wiring instructions/diagrams, please see the :ref:`TRANSLATED TEXT <docs/zero-to-robot/step-1/how-to-wire-a-robot:How to Wire an FRC Robot>`

Publishing Translations
-----------------------

Translations are pulled from Transifex and published automatically each day.

Accuracy
--------

Translations should be accurate to the original text. If improvements to the English text can be made, open a PR or issue on the `6940swerve-docs <https://github.com/mendax1234/6940Swerve-docs>`_ repository. These can then get translated on merge.  