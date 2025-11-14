Contributing
============

Contributions to CubeForge are welcome! This page explains how to contribute to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/Teddy-van-Jerry/cubeforge.git
      cd cubeforge

3. Install the package in development mode:

   .. code-block:: bash

      pip install -e .

4. Create a new branch for your changes:

   .. code-block:: bash

      git checkout -b feature/my-new-feature

Development Workflow
--------------------

Testing
~~~~~~~

CubeForge currently uses example-based testing. Run the examples to verify functionality:

.. code-block:: bash

   python examples/create_shapes.py
   python examples/coordinate_systems.py
   python examples/mesh_optimization.py

All examples should run without errors and produce valid STL files.

Code Style
~~~~~~~~~~

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and modular

Documentation
~~~~~~~~~~~~~

When adding new features:

1. Update relevant documentation in ``docs/``
2. Add examples demonstrating the feature
3. Update the changelog in ``docs/changelog.rst``

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

To build documentation locally:

.. code-block:: bash

   cd docs
   pip install -r requirements.txt
   make html

The built documentation will be in ``docs/_build/html/``.

Submitting Changes
------------------

1. Commit your changes with a clear commit message:

   .. code-block:: bash

      git add .
      git commit -m "Add feature: description of feature"

2. Push to your fork:

   .. code-block:: bash

      git push origin feature/my-new-feature

3. Open a pull request on GitHub

4. Wait for review and address any feedback

Pull Request Guidelines
------------------------

- **One feature per PR:** Keep pull requests focused on a single feature or fix
- **Clear description:** Explain what your changes do and why
- **Test your changes:** Ensure examples run successfully
- **Update documentation:** Include relevant documentation updates
- **Follow code style:** Maintain consistency with existing code

Reporting Issues
----------------

If you find a bug or have a feature request:

1. Check if the issue already exists in the `issue tracker <https://github.com/Teddy-van-Jerry/cubeforge/issues>`_
2. If not, create a new issue with:

   - Clear description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Python version and operating system
   - Minimal code example (if applicable)

Areas for Contribution
----------------------

Some areas where contributions would be particularly welcome:

- **Additional export formats:** OBJ, PLY, etc.
- **Import functionality:** Load existing meshes
- **Performance optimizations:** Faster mesh generation
- **Unit tests:** Comprehensive test suite
- **Examples:** More complex use cases
- **Documentation:** Improved guides and tutorials

Code of Conduct
---------------

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment
- Follow the project's coding standards

License
-------

By contributing to CubeForge, you agree that your contributions will be licensed under the MIT License.

Questions?
----------

If you have questions about contributing, feel free to:

- Open a discussion on GitHub
- Ask in a pull request
- Contact the maintainers

Thank you for contributing to CubeForge!
