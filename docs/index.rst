Image Differ
============

Image Differ is a tool for image comparison. It loads 2 images and generates the diff image that shows where the images
are different. It also calculates:

   - Percentage of pixels where the images differ (with adjustable threshold for difference)
   - Mean Square Error for the images
   - Structural Similarity Index

It can also calculate comparison stats for individual color channels or ignore colors.

All the functions for image comparison and manipulations are separated in ``imagediffer.core`` module and can be reused
without the application.

Submodules
==========

.. toctree::

    imagediffer.app
    imagediffer.core



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. raw:: html

    <a href="https://github.com/janslifka/image-differ"><img style="position: absolute; top: 0; right: 0; border: 0;"
       src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png"></a>
