# ADR 001: Switch to Rustler and Rust-FUSE

## Context

The initial implementation of the FUSE filesystem in Elixir using `elixir-userfs` faced several challenges:

- **Outdated Dependencies**: The existing implementation relied on outdated dependencies that were difficult to maintain and update. The most basic "Hello, World!" example wouldn't compile on Elixir 1.17, as it was expecting Elixir 1.5, which is significantly outdated.
- **Compatibility Issues**: Integrating with macFUSE on macOS had compatibility issues that were difficult to resolve with the current setup.
- **Mounting Issues**: We couldn't get an instance to successfully mount into the filesystem.

## Decision

Switch to using `rustler` and `rust-fuse` for the FUSE implementation in the `command_fs` project.

- **Rustler**: Provides a safe and efficient way to write NIFs for Elixir, allowing seamless integration with Rust code.
- **Rust-FUSE**: Offers a more robust and idiomatic way to implement FUSE filesystems, leveraging Rust's performance and safety features.

## Consequences

- **Improved Performance**: Expect significant performance improvements due to Rust's efficiency and concurrency model.
- **Simplified Codebase**: Reduce complexity by offloading FUSE operations to Rust, allowing Elixir to focus on higher-level logic.
- **Better Error Handling**: Utilize Rust's safety features to handle errors more gracefully and prevent common issues.

## Status

Rejected - Decided to take a different approach based on the stack-reference.md implementation plan.

## Date

2024-11-29

## Author

Project Team

## Related Epics

- Epic 2: Migration to Rust Implementation of UserFS

## References

- [Rustler Documentation](https://github.com/rusterlium/rustler)
- [Rust-FUSE Documentation](https://github.com/zargony/rust-fuse)
