# Parallelization

1. Parallelize only when the tests are data-isolated.
2. Keep unique test data across workers.
3. Avoid shared mutable global state in Rest Assured setup.
