Contributing Guidelines
=======================

Welcome to the contribution guidelines for the 6940swerve-docs project. If you are unfamiliar to writing in the reStructuredText format, please read up on it `here <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`__.

Creating a PR
-------------

PRs should be made to the `6940swerve-docs <https://github.com/mendax1234/6940swerve-docs>`__ repo on GitHub. They should point to the ``main`` branch and *not* ``stable``.

Creating New Content
--------------------

Thanks for contributing to the `6940swerve-docs <https://github.com/mendax1234/6940swerve-docs>`__ project! There are a couple things you should know before getting started!

Where to place articles?
^^^^^^^^^^^^^^^^^^^^^^^^

The location for new articles can be a pretty opinionated subject. Standalone articles that fall well into an already subject category should be placed into mentioned subject category (documentation on something about simulation should be placed into the simulation section). However, things can get pretty complicated when an article combines or references two separate existing sections. In this situation, we advise the author to open an issue on the repository to get discussion going before opening the PR.

.. note:: All new articles will undergo a review process before being merged into the repository. This review process will be done by members of the WPILib team. New Articles must be on official *FIRST* supported Software and Hardware. Documentation on unofficial libraries or sensors *will not* be accepted. This process may take some time to review, please be patient.

Where to place sections?
^^^^^^^^^^^^^^^^^^^^^^^^

Sections are quite tricky, as they contain a large amount of content. We advise the author to open an `issue <https://github.com/mendax1234/6940swerve-docs/issues>`__ to gather discussion before opening up a PR.

Linking Other Articles
^^^^^^^^^^^^^^^^^^^^^^

In the instance that the article references content that is described in another article, the author should make best effort to link to that article upon the first reference.

Imagine we have the following content in a drivetrain tutorial:

.. code-block:: text

   Teams may often need to test their robot code outside of a competition. :ref:`Simulation <link-to-simulation:simulation>` is a means to achieve this. Simulation offers teams a way to unit test and test their robot code without ever needing a robot.

Notice how only the first instance of Simulation is linked. This is the structure the author should follow. There are times where a linked article has different topics of content. If you reference the different types of content in the article, you should link to each new reference once (except in situations where the author has deemed it appropriate otherwise).
