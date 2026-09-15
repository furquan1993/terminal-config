# Gradle review

Apply this reference whenever the PR changes Gradle build behavior, including
scripts, plugins, wrapper files, version catalogs, or Gradle-related CI commands.
Review both correctness and documented practices; identify recommendations as
such instead of presenting every practice as a functional bug.

## Establish the version and purpose

Read `gradle/wrapper/gradle-wrapper.properties`, build/settings files, plugin
versions, catalogs, toolchains, and relevant build logic. If the wrapper changes,
review compatibility across both versions and the migration notes. Establish the
actual JDK used to run Gradle separately from compile/test toolchains.

Use official documentation for the detected Gradle/plugin versions. The sources
below are discovery entrypoints; replace `/current/` with the verified version
when that documentation exists. Do not copy a newly introduced API into an older
build, prescribe a version upgrade unrelated to the PR, or mandate switching
between Groovy and Kotlin DSL.

## Review the changed behavior

- **Plugin application and lifecycle:** Check plugin order assumptions, extension
  availability, convention plugin boundaries, and changes to `afterEvaluate` or
  cross-project configuration. Prefer supported plugin callbacks and lazy property
  wiring when applicable; explain a concrete ordering or maintenance concern.
- **Task wiring and data flow:** Trace producers and consumers through providers,
  task dependencies, file collections, and declared inputs/outputs. Check that
  required tasks actually execute and generated outputs reach their consumers.
  `mustRunAfter` alone must not be mistaken for scheduling a dependency.
- **Lazy configuration:** Assess appropriate use of `tasks.register`, `named`,
  `configureEach`, and provider-backed values for the version in use. Check early
  configuration resolution and mutation of other tasks during lazy configuration.
  Treat this as Gradle practice/build-behavior review, without adding benchmarking
  or general performance-regression analysis.
- **Repeatable task results:** Check input/output declarations and task actions
  against the real files and external inputs they use. If the project enables
  up-to-date checks, caching, or configuration cache, ensure the change preserves
  their correctness; do not mandate enabling optional features as unrelated work.
- **Dependencies and repositories:** Validate configurations (`api`,
  `implementation`, runtime/test scopes), constraints/platforms, catalog aliases,
  resolution rules, repository availability, and plugin-management placement.
  Identify changes that select the wrong artifacts, omit needed runtime inputs,
  or alter consumers' dependency contracts.
- **Toolchains and compatibility:** Check wrapper/JDK/plugin compatibility and
  whether compile and test settings match the intended target runtime.
- **Artifacts and publication configuration:** Inspect coordinates, variants,
  metadata, and task wiring when changed. Do not run real publication or release
  tasks. Use repository fixtures or non-publishing validation to check behavior.
- **Tests for build logic:** Inspect assertions for custom tasks/plugins and
  relevant TestKit functional tests, including failure paths. A passing `help`
  task alone does not validate task execution, artifact contents, or consumer
  behavior. Functional TestKit results support Gradle correctness but must not be
  mislabeled as unit-line coverage.

Run only existing relevant verification tasks after inspecting what they do.
Discover task names rather than assuming every repository has `spotlessCheck`,
`validatePlugins`, or `jacocoTestReport`. Start with affected modules/build logic;
broaden to consumers when the change's impact requires it. Report unavailable
checks, and compare a failing behavior with the base to avoid pre-existing noise.

## Source entrypoints

- [Gradle best practices](https://docs.gradle.org/current/userguide/best_practices.html)
- [General build practices](https://docs.gradle.org/current/userguide/best_practices_general.html)
- [Task practices](https://docs.gradle.org/current/userguide/best_practices_tasks.html)
- [Task configuration avoidance](https://docs.gradle.org/current/userguide/task_configuration_avoidance.html)
- [Testing Gradle plugins](https://docs.gradle.org/current/userguide/testing_gradle_plugins.html)
- [Compatibility matrix](https://docs.gradle.org/current/userguide/compatibility.html)

Research additional official plugin documentation and community examples when
they clarify an actual finding. Include relevant source links in the proposed
comment; keep generic reading lists out of GitHub comments.
